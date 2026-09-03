from pydantic import BaseModel, ConfigDict
from datetime import date, time


class ClienteBase(BaseModel):
    nome: str
    telefone: str
    endereco: str | None = None


class ClienteCreate(ClienteBase):
    """Usado quando o adestrador envia dados para criar/editar um cliente."""
    pass


class ClienteOut(ClienteBase):
    """Usado quando a API devolve um cliente já salvo no banco."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class CachorroBase(BaseModel):
    nome: str
    raca: str | None = None
    idade: int | None = None
    sexo: str | None = None
    cliente_id: int


class CachorroCreate(CachorroBase):
    """Usado quando o adestrador envia dados para criar/editar um cachorro."""
    pass


class CachorroOut(CachorroBase):
    """Usado quando a API devolve um cachorro já salvo no banco."""
    id: int
    cliente: ClienteOut  # <-- devolve o cliente inteiro, não só o ID

    model_config = ConfigDict(from_attributes=True)


class FichaAvaliacaoBase(BaseModel):
    queixa_principal: str | None = None
    historico_comportamento: str | None = None
    expectativa_dono: str | None = None


class FichaAvaliacaoCreate(FichaAvaliacaoBase):
    """Usado tanto para criar quanto para editar a ficha."""
    pass


class FichaAvaliacaoOut(FichaAvaliacaoBase):
    id: int
    cachorro_id: int

    model_config = ConfigDict(from_attributes=True)


class PlanoBase(BaseModel):
    nome: str
    quantidade_sessoes: int


class PlanoCreate(PlanoBase):
    """Usado para criar ou editar um plano."""
    pass


class PlanoOut(PlanoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


from app.models import StatusSessao


class AgendamentoBase(BaseModel):
    data: date
    horario: time
    cliente_id: int
    cachorro_id: int
    plano_id: int


class AgendamentoCreate(AgendamentoBase):
    """Usado para criar um novo agendamento. O status sempre começa como 'Agendada'."""
    pass


class AgendamentoUpdate(AgendamentoBase):
    """Usado para editar os dados gerais (data, horário, cliente, cachorro, plano)."""
    pass


class StatusUpdate(BaseModel):
    """Usado apenas para marcar a sessão como Agendada/Concluída."""
    status: StatusSessao


class AnotacoesUpdate(BaseModel):
    """Usado apenas para escrever/editar o diário de bordo da sessão."""
    anotacoes: str | None = None


class AgendamentoOut(BaseModel):
    id: int
    data: date
    horario: time
    status: StatusSessao
    anotacoes: str | None = None
    cliente: ClienteOut
    cachorro: CachorroOut
    plano: PlanoOut

    model_config = ConfigDict(from_attributes=True)

