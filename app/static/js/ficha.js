const formulario = document.getElementById("form-ficha");
const cachorroId = formulario.dataset.cachorroId;
const API_FICHA = `/api/cachorros/${cachorroId}/ficha`;
const API_CACHORRO = `/api/cachorros/${cachorroId}`;

const campoQueixa = document.getElementById("queixa_principal");
const campoHistorico = document.getElementById("historico_comportamento");
const campoExpectativa = document.getElementById("expectativa_dono");
const tituloCachorro = document.getElementById("titulo-cachorro");
const mensagemStatus = document.getElementById("mensagem-status");

async function carregarNomeCachorro() {
    const resposta = await fetch(API_CACHORRO, { credentials: "same-origin" });
    if (!resposta.ok) return;

    const cachorro = await resposta.json();
    tituloCachorro.textContent = `Ficha de Avaliação — ${cachorro.nome}`;
}

async function carregarFicha() {
    const resposta = await fetch(API_FICHA, { credentials: "same-origin" });

    // Um 404 aqui é esperado quando a ficha ainda não foi criada — não é erro real,
    // só significa "formulário em branco, pronto para a primeira ficha".
    if (!resposta.ok) return;

    const ficha = await resposta.json();
    campoQueixa.value = ficha.queixa_principal ?? "";
    campoHistorico.value = ficha.historico_comportamento ?? "";
    campoExpectativa.value = ficha.expectativa_dono ?? "";
}

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dados = {
        queixa_principal: campoQueixa.value || null,
        historico_comportamento: campoHistorico.value || null,
        expectativa_dono: campoExpectativa.value || null,
    };

    const resposta = await fetch(API_FICHA, {
        method: "PUT",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
    });

    if (!resposta.ok) {
        alert("Erro ao salvar a ficha de avaliação.");
        return;
    }

    mensagemStatus.textContent = "Ficha salva com sucesso!";
    mensagemStatus.className = "mensagem-sucesso";
    mensagemStatus.hidden = false;
    setTimeout(() => { mensagemStatus.hidden = true; }, 3000);
});

carregarNomeCachorro();
carregarFicha();
