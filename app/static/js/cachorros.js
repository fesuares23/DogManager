const API_CACHORROS = "/api/cachorros/";

const API_CLIENTES = "/api/clientes/";

const formulario = document.getElementById("form-cachorro");

const campoId = document.getElementById("cachorro-id");

const campoNome = document.getElementById("nome");

const campoRaca = document.getElementById("raca");

const campoIdade = document.getElementById("idade");

const campoSexo = document.getElementById("sexo");

const campoCliente = document.getElementById("cliente_id");

const tituloFormulario = document.getElementById("titulo-formulario");

const botaoCancelar = document.getElementById("botao-cancelar");

const corpoTabela = document.getElementById("corpo-tabela");

const mensagemVazia = document.getElementById("mensagem-lista-vazia");

async function carregarClientesNoSelect() {

    const resposta = await fetch(API_CLIENTES, { credentials: "same-origin" });

    const clientes = await resposta.json();

    if (clientes.length === 0) {

        campoCliente.innerHTML = `<option value="">Cadastre um cliente primeiro</option>`;

        return;
    }

    campoCliente.innerHTML = `<option value="">Selecione o cliente</option>` +

        clientes.map(c => `<option value="${c.id}">${c.nome}</option>`).join("");
}

async function carregarCachorros() {

    const resposta = await fetch(API_CACHORROS, { credentials: "same-origin" });

    if (!resposta.ok) {

        alert("Não foi possível carregar os cachorros.");

        return;
    }

    const cachorros = await resposta.json();

    desenharTabela(cachorros);
}

function desenharTabela(cachorros) {

    corpoTabela.innerHTML = "";

    if (cachorros.length === 0) {

        mensagemVazia.hidden = false;

        return;
    }

    mensagemVazia.hidden = true;

    for (const cachorro of cachorros) {

        const linha = document.createElement("tr");

        linha.innerHTML = `

            <td>${cachorro.nome}</td>

            <td>${cachorro.raca ?? ""}</td>

            <td>${cachorro.idade ?? ""}</td>

            <td>${cachorro.sexo ?? ""}</td>

            <td>${cachorro.cliente.nome}</td>

            <td>

                <a class="botao-acao botao-ficha" href="/cachorros/${cachorro.id}/ficha">Ficha</a>

                <button class="botao-acao botao-editar" data-id="${cachorro.id}">Editar</button>

                <button class="botao-acao botao-excluir" data-id="${cachorro.id}">Excluir</button>

            </td>

        `;

        corpoTabela.appendChild(linha);
    }
}

formulario.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const dados = {

        nome: campoNome.value,

        raca: campoRaca.value || null,

        idade: campoIdade.value ? Number(campoIdade.value) : null,

        sexo: campoSexo.value || null,

        cliente_id: Number(campoCliente.value),

    };

    const id = campoId.value;

    const url = id ? `${API_CACHORROS}${id}` : API_CACHORROS;

    const metodo = id ? "PUT" : "POST";

    const resposta = await fetch(url, {

        method: metodo,

        credentials: "same-origin",

        headers: { "Content-Type": "application/json" },

        body: JSON.stringify(dados),

    });

    if (!resposta.ok) {

        alert("Erro ao salvar o cachorro. Confira os dados e tente novamente.");

        return;
    }

    limparFormulario();

    carregarCachorros();
});

corpoTabela.addEventListener("click", async (evento) => {

    const botao = evento.target;

    const id = botao.dataset.id;

    if (!id) return;

    if (botao.classList.contains("botao-editar")) {

        const resposta = await fetch(`${API_CACHORROS}${id}`, { credentials: "same-origin" });

        const cachorro = await resposta.json();

        preencherFormularioParaEdicao(cachorro);
    }

    if (botao.classList.contains("botao-excluir")) {

        const confirmou = confirm(

            "Tem certeza que deseja excluir este cachorro? A ficha de avaliação dele também será excluída."

        );

        if (!confirmou) return;

        const resposta = await fetch(`${API_CACHORROS}${id}`, {

            method: "DELETE",

            credentials: "same-origin",

        });

        if (!resposta.ok) {

            const erro = await resposta.json().catch(() => null);

            alert(erro?.detail || "Não foi possível excluir este cachorro.");

            return;
        }

        carregarCachorros();
    }
});

function preencherFormularioParaEdicao(cachorro) {

    campoId.value = cachorro.id;

    campoNome.value = cachorro.nome;

    campoRaca.value = cachorro.raca ?? "";

    campoIdade.value = cachorro.idade ?? "";

    campoSexo.value = cachorro.sexo ?? "";

    campoCliente.value = cachorro.cliente_id;

    tituloFormulario.textContent = "Editar cachorro";

    botaoCancelar.hidden = false;

    campoNome.focus();
}

function limparFormulario() {

    formulario.reset();

    campoId.value = "";

    tituloFormulario.textContent = "Novo cachorro";

    botaoCancelar.hidden = true;
}

botaoCancelar.addEventListener("click", limparFormulario);

async function iniciar() {

    await carregarClientesNoSelect();

    await carregarCachorros();
}

iniciar();
