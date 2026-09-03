const API_URL = "/api/clientes/";

const formulario = document.getElementById("form-cliente");
const campoId = document.getElementById("cliente-id");
const campoNome = document.getElementById("nome");
const campoTelefone = document.getElementById("telefone");
const campoEndereco = document.getElementById("endereco");
const tituloFormulario = document.getElementById("titulo-formulario");
const botaoCancelar = document.getElementById("botao-cancelar");
const corpoTabela = document.getElementById("corpo-tabela");
const mensagemVazia = document.getElementById("mensagem-lista-vazia");

async function carregarClientes() {
    const resposta = await fetch(API_URL, { credentials: "same-origin" });

    if (!resposta.ok) {
        alert("Não foi possível carregar os clientes.");
        return;
    }

    const clientes = await resposta.json();
    desenharTabela(clientes);
}

function desenharTabela(clientes) {
    corpoTabela.innerHTML = "";

    if (clientes.length === 0) {
        mensagemVazia.hidden = false;
        return;
    }
    mensagemVazia.hidden = true;

    for (const cliente of clientes) {
        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${cliente.nome}</td>
            <td>${cliente.telefone}</td>
            <td>${cliente.endereco ?? ""}</td>
            <td>
                <button class="botao-acao botao-editar" data-id="${cliente.id}">Editar</button>
                <button class="botao-acao botao-excluir" data-id="${cliente.id}">Excluir</button>
            </td>
        `;
        corpoTabela.appendChild(linha);
    }
}

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dados = {
        nome: campoNome.value,
        telefone: campoTelefone.value,
        endereco: campoEndereco.value || null,
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
        alert("Erro ao salvar o cliente. Confira os dados e tente novamente.");
        return;
    }

    limparFormulario();
    carregarClientes();
});

corpoTabela.addEventListener("click", async (evento) => {
    const botao = evento.target;
    const id = botao.dataset.id;
    if (!id) return;

    if (botao.classList.contains("botao-editar")) {
        const resposta = await fetch(`${API_URL}${id}`, { credentials: "same-origin" });
        const cliente = await resposta.json();
        preencherFormularioParaEdicao(cliente);
    }

    if (botao.classList.contains("botao-excluir")) {
        const confirmou = confirm(
            "Tem certeza que deseja excluir este cliente? Os cachorros vinculados a ele também serão excluídos."
        );
        if (!confirmou) return;

        const resposta = await fetch(`${API_URL}${id}`, {
            method: "DELETE",
            credentials: "same-origin",
        });

        if (!resposta.ok) {
    const erro = await resposta.json().catch(() => null);
    alert(erro?.detail || "Não foi possível excluir este cliente.");
    return;
}
        carregarClientes();
    }
});

function preencherFormularioParaEdicao(cliente) {
    campoId.value = cliente.id;
    campoNome.value = cliente.nome;
    campoTelefone.value = cliente.telefone;
    campoEndereco.value = cliente.endereco ?? "";
    tituloFormulario.textContent = "Editar cliente";
    botaoCancelar.hidden = false;
    campoNome.focus();
}

function limparFormulario() {
    formulario.reset();
    campoId.value = "";
    tituloFormulario.textContent = "Novo cliente";
    botaoCancelar.hidden = true;
}

botaoCancelar.addEventListener("click", limparFormulario);

carregarClientes();
