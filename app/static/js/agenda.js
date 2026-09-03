const API_AGENDA = "/api/agenda/";
const API_CLIENTES = "/api/clientes/";
const API_CACHORROS = "/api/cachorros/";
const API_PLANOS = "/api/planos/";

const formulario = document.getElementById("form-agendamento");
const campoId = document.getElementById("agendamento-id");
const campoData = document.getElementById("data");
const campoHorario = document.getElementById("horario");
const campoCliente = document.getElementById("cliente_id");
const campoCachorro = document.getElementById("cachorro_id");
const campoPlano = document.getElementById("plano_id");
const tituloFormulario = document.getElementById("titulo-formulario");
const botaoCancelar = document.getElementById("botao-cancelar");
const corpoTabela = document.getElementById("corpo-tabela");
const mensagemVazia = document.getElementById("mensagem-lista-vazia");

async function carregarSelects() {
    const [respClientes, respCachorros, respPlanos] = await Promise.all([
        fetch(API_CLIENTES, { credentials: "same-origin" }),
        fetch(API_CACHORROS, { credentials: "same-origin" }),
        fetch(API_PLANOS, { credentials: "same-origin" }),
    ]);

    const clientes = await respClientes.json();
    const cachorros = await respCachorros.json();
    const planos = await respPlanos.json();

    campoCliente.innerHTML = clientes.length
        ? `<option value="">Selecione o cliente</option>` + clientes.map(c => `<option value="${c.id}">${c.nome}</option>`).join("")
        : `<option value="">Cadastre um cliente primeiro</option>`;

    campoCachorro.innerHTML = cachorros.length
        ? `<option value="">Selecione o cachorro</option>` + cachorros.map(c => `<option value="${c.id}">${c.nome} (dono: ${c.cliente.nome})</option>`).join("")
        : `<option value="">Cadastre um cachorro primeiro</option>`;

    campoPlano.innerHTML = planos.length
        ? `<option value="">Selecione o plano</option>` + planos.map(p => `<option value="${p.id}">${p.nome} (${p.quantidade_sessoes} sessões)</option>`).join("")
        : `<option value="">Cadastre um plano primeiro</option>`;
}

async function carregarAgendamentos() {
    const resposta = await fetch(API_AGENDA, { credentials: "same-origin" });

    if (!resposta.ok) {
        alert("Não foi possível carregar a agenda.");
        return;
    }

    const agendamentos = await resposta.json();
    desenharTabela(agendamentos);
}

function desenharTabela(agendamentos) {
    corpoTabela.innerHTML = "";

    if (agendamentos.length === 0) {
        mensagemVazia.hidden = false;
        return;
    }
    mensagemVazia.hidden = true;

    for (const ag of agendamentos) {
        const concluida = ag.status === "Concluída";
        const classeStatus = concluida ? "status-concluida" : "status-agendada";
        const textoBotaoStatus = concluida ? "Reabrir" : "Marcar concluída";

        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${formatarData(ag.data)}</td>
            <td>${ag.horario.slice(0, 5)}</td>
            <td>${ag.cliente.nome}</td>
            <td>${ag.cachorro.nome}</td>
            <td>${ag.plano.nome}</td>
            <td><span class="status-badge ${classeStatus}">${ag.status}</span></td>
            <td>
                <button class="botao-acao botao-status" data-id="${ag.id}" data-status-atual="${ag.status}">${textoBotaoStatus}</button>
                <a class="botao-acao botao-diario" href="/agenda/${ag.id}/anotacoes">Diário</a>
                <button class="botao-acao botao-editar" data-id="${ag.id}">Editar</button>
                <button class="botao-acao botao-excluir" data-id="${ag.id}">Excluir</button>
            </td>
        `;
        corpoTabela.appendChild(linha);
    }
}

function formatarData(dataIso) {
    const [ano, mes, dia] = dataIso.split("-");
    return `${dia}/${mes}/${ano}`;
}

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dados = {
        data: campoData.value,
        horario: campoHorario.value,
        cliente_id: Number(campoCliente.value),
        cachorro_id: Number(campoCachorro.value),
        plano_id: Number(campoPlano.value),
    };

    const id = campoId.value;
    const url = id ? `${API_AGENDA}${id}` : API_AGENDA;
    const metodo = id ? "PUT" : "POST";

    const resposta = await fetch(url, {
        method: metodo,
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
    });

    if (!resposta.ok) {
        alert("Erro ao salvar o agendamento. Confira os dados e tente novamente.");
        return;
    }

    limparFormulario();
    carregarAgendamentos();
});

corpoTabela.addEventListener("click", async (evento) => {
    const botao = evento.target;
    const id = botao.dataset.id;
    if (!id) return;

    if (botao.classList.contains("botao-editar")) {
        const resposta = await fetch(`${API_AGENDA}${id}`, { credentials: "same-origin" });
        const agendamento = await resposta.json();
        preencherFormularioParaEdicao(agendamento);
    }

    if (botao.classList.contains("botao-status")) {
        const statusAtual = botao.dataset.statusAtual;
        const novoStatus = statusAtual === "Concluída" ? "Agendada" : "Concluída";

        const resposta = await fetch(`${API_AGENDA}${id}/status`, {
            method: "PATCH",
            credentials: "same-origin",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: novoStatus }),
        });

        if (!resposta.ok) {
            alert("Não foi possível atualizar o status.");
            return;
        }
        carregarAgendamentos();
    }

    if (botao.classList.contains("botao-excluir")) {
        const confirmou = confirm("Tem certeza que deseja excluir este agendamento? As anotações dele também serão perdidas.");
        if (!confirmou) return;

        const resposta = await fetch(`${API_AGENDA}${id}`, {
            method: "DELETE",
            credentials: "same-origin",
        });

        if (!resposta.ok) {
            alert("Não foi possível excluir este agendamento.");
            return;
        }
        carregarAgendamentos();
    }
});

function preencherFormularioParaEdicao(agendamento) {
    campoId.value = agendamento.id;
    campoData.value = agendamento.data;
    campoHorario.value = agendamento.horario.slice(0, 5);
    campoCliente.value = agendamento.cliente.id;
    campoCachorro.value = agendamento.cachorro.id;
    campoPlano.value = agendamento.plano.id;
    tituloFormulario.textContent = "Editar agendamento";
    botaoCancelar.hidden = false;
    campoData.focus();
}

function limparFormulario() {
    formulario.reset();
    campoId.value = "";
    tituloFormulario.textContent = "Novo agendamento";
    botaoCancelar.hidden = true;
}

botaoCancelar.addEventListener("click", limparFormulario);

async function iniciar() {
    await carregarSelects();
    await carregarAgendamentos();
}

iniciar();
