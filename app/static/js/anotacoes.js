const formulario = document.getElementById("form-anotacoes");
const agendamentoId = formulario.dataset.agendamentoId;
const API_AGENDAMENTO = `/api/agenda/${agendamentoId}`;
const API_ANOTACOES = `/api/agenda/${agendamentoId}/anotacoes`;

const campoAnotacoes = document.getElementById("anotacoes");
const tituloSessao = document.getElementById("titulo-sessao");
const mensagemStatus = document.getElementById("mensagem-status");

async function carregarAgendamento() {
    const resposta = await fetch(API_AGENDAMENTO, { credentials: "same-origin" });
    if (!resposta.ok) return;

    const agendamento = await resposta.json();
    const [ano, mes, dia] = agendamento.data.split("-");
    tituloSessao.textContent =
        `Diário de Bordo — ${agendamento.cachorro.nome} (${dia}/${mes}/${ano} às ${agendamento.horario.slice(0, 5)})`;
    campoAnotacoes.value = agendamento.anotacoes ?? "";
}

formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const resposta = await fetch(API_ANOTACOES, {
        method: "PUT",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ anotacoes: campoAnotacoes.value || null }),
    });

    if (!resposta.ok) {
        alert("Erro ao salvar as anotações.");
        return;
    }

    mensagemStatus.textContent = "Anotações salvas com sucesso!";
    mensagemStatus.className = "mensagem-sucesso";
    mensagemStatus.hidden = false;
    setTimeout(() => { mensagemStatus.hidden = true; }, 3000);
});

carregarAgendamento();
