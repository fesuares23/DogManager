
const API_URL = "/api/planos/";

const formulario = document.getElementById("form-plano");

const campoId = document.getElementById("plano-id");

const campoNome = document.getElementById("nome");

const campoSessoes = document.getElementById("quantidade_sessoes");

const tituloFormulario = document.getElementById("titulo-formulario");

const botaoCancelar = document.getElementById("botao-cancelar");

const corpoTabela = document.getElementById("corpo-tabela");

const mensagemVazia = document.getElementById("mensagem-lista-vazia");

async function carregarPlanos() {

    const resposta = await fetch(API_URL, { credentials: "same-origin" });

    if (!resposta.ok) {

        alert("Não foi possível carregar os planos.");

        return;
    }

    const planos = await resposta.json();

    desenharTabela(planos);
}

function desenharTabela(planos) {

    corpoTabela.innerHTML = "";

    if (planos.length === 0) {

        mensagemVazia.hidden = false;

        return;
    }

    mensagemVazia.hidden = true;

    for (const plano of planos) {

        const linha = document.createElement("tr");

        linha.innerHTML = `

            <td>${plano.nome}</td>

            <td>${plano.quantidade_sessoes}</td>

            <td>

                <button class="botao-acao botao-editar" data-id="${plano.id}">Editar</button>

                <button class="botao-acao botao-excluir" data-id="${plano.id}">Excluir</button>

            </td>

        `;

        corpoTabela.appendChild(linha);
    }
}

formulario.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const dados = {

        nome: campoNome.value,

        quantidade_sessoes: Number(campoSessoes.value),

    };

    const id = campoId.value;

    const url = id ? `${API_URL}${id}` : API_URL;

    const metodo = id ? "PUT" : "POST";

    const resposta = await fetch(url, {

        method: metodo,

        credentials: "same-origin",

        headers: { "Content-Type": "application/json" },

        body: JSON.stringify(dados),

    });

    if (!resposta.ok) {

        alert("Erro ao salvar o plano. Confira os dados e tente novamente.");

        return;
    }

    limparFormulario();

    carregarPlanos();
});

corpoTabela.addEventListener("click", async (evento) => {

    const botao = evento.target;

    const id = botao.dataset.id;

    if (!id) return;

    if (botao.classList.contains("botao-editar")) {

        const resposta = await fetch(`${API_URL}${id}`, { credentials: "same-origin" });

        const plano = await resposta.json();

        preencherFormularioParaEdicao(plano);
    }

    if (botao.classList.contains("botao-excluir")) {

        const confirmou = confirm(

            "Tem certeza que deseja excluir este plano? Agendamentos que já usam esse plano podem ficar inconsistentes."

        );

        if (!confirmou) return;

        const resposta = await fetch(`${API_URL}${id}`, {

            method: "DELETE",

            credentials: "same-origin",

        });

        if (!resposta.ok) {

            const erro = await resposta.json().catch(() => null);

            alert(erro?.detail || "Não foi possível excluir este plano.");

            return;
        }

        carregarPlanos();
    }
});

function preencherFormularioParaEdicao(plano) {

    campoId.value = plano.id;

    campoNome.value = plano.nome;

    campoSessoes.value = plano.quantidade_sessoes;

    tituloFormulario.textContent = "Editar plano";

    botaoCancelar.hidden = false;

    campoNome.focus();
}

function limparFormulario() {

    formulario.reset();

    campoId.value = "";

    tituloFormulario.textContent = "Novo plano";

    botaoCancelar.hidden = true;
}

botaoCancelar.addEventListener("click", limparFormulario);

carregarPlanos();

