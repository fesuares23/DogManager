import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, Time, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=True)

    # relationship() não cria uma coluna no banco — ela apenas ensina
    # o SQLAlchemy a "navegar" de um Cliente até a lista de seus Cachorros.
    cachorros = relationship("Cachorro", back_populates="cliente", cascade="all, delete-orphan")


class Cachorro(Base):
    __tablename__ = "cachorros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    raca = Column(String, nullable=True)
    idade = Column(Integer, nullable=True)
    sexo = Column(String, nullable=True)

    # ForeignKey cria de fato a coluna no banco que guarda o ID do cliente dono.
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="cachorros")
    ficha_avaliacao = relationship(
        "FichaAvaliacao", back_populates="cachorro",
        uselist=False, cascade="all, delete-orphan"
    )


class FichaAvaliacao(Base):
    __tablename__ = "fichas_avaliacao"

    id = Column(Integer, primary_key=True, index=True)
    cachorro_id = Column(Integer, ForeignKey("cachorros.id"), nullable=False, unique=True)
    queixa_principal = Column(Text, nullable=True)
    historico_comportamento = Column(Text, nullable=True)
    expectativa_dono = Column(Text, nullable=True)

    cachorro = relationship("Cachorro", back_populates="ficha_avaliacao")


class Plano(Base):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    quantidade_sessoes = Column(Integer, nullable=False)


class StatusSessao(str, enum.Enum):
    AGENDADA = "Agendada"
    CONCLUIDA = "Concluída"


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date, nullable=False)
    horario = Column(Time, nullable=False)
    status = Column(Enum(StatusSessao), default=StatusSessao.AGENDADA, nullable=False)
    anotacoes = Column(Text, nullable=True)

    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    cachorro_id = Column(Integer, ForeignKey("cachorros.id"), nullable=False)
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=False)

    cliente = relationship("Cliente")
    cachorro = relationship("Cachorro")
    plano = relationship("Plano")


class Credencial(Base):
    __tablename__ = "credenciais"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    salt = Column(String, nullable=False)

