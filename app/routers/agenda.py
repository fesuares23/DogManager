from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/agenda", tags=["Agenda"])


def _validar_referencias(db: Session, cliente_id: int, cachorro_id: int, plano_id: int):
    """Confirma que o cliente, o cachorro e o plano informados realmente existem."""
    if not db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first():
        raise HTTPException(status_code=404, detail="Cliente informado não existe")
    if not db.query(models.Cachorro).filter(models.Cachorro.id == cachorro_id).first():
        raise HTTPException(status_code=404, detail="Cachorro informado não existe")
    if not db.query(models.Plano).filter(models.Plano.id == plano_id).first():
        raise HTTPException(status_code=404, detail="Plano informado não existe")


@router.get("/", response_model=list[schemas.AgendamentoOut])
def listar_agendamentos(db: Session = Depends(get_db)):
    return (
        db.query(models.Agendamento)
        .order_by(models.Agendamento.data, models.Agendamento.horario)
        .all()
    )


@router.get("/{agendamento_id}", response_model=schemas.AgendamentoOut)
def obter_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return agendamento


@router.post("/", response_model=schemas.AgendamentoOut, status_code=201)
def criar_agendamento(dados: schemas.AgendamentoCreate, db: Session = Depends(get_db)):
    _validar_referencias(db, dados.cliente_id, dados.cachorro_id, dados.plano_id)

    novo_agendamento = models.Agendamento(
        data=dados.data,
        horario=dados.horario,
        cliente_id=dados.cliente_id,
        cachorro_id=dados.cachorro_id,
        plano_id=dados.plano_id,
        status=models.StatusSessao.AGENDADA,
    )
    db.add(novo_agendamento)
    db.commit()
    db.refresh(novo_agendamento)
    return novo_agendamento


@router.put("/{agendamento_id}", response_model=schemas.AgendamentoOut)
def atualizar_agendamento(agendamento_id: int, dados: schemas.AgendamentoUpdate, db: Session = Depends(get_db)):
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    _validar_referencias(db, dados.cliente_id, dados.cachorro_id, dados.plano_id)

    agendamento.data = dados.data
    agendamento.horario = dados.horario
    agendamento.cliente_id = dados.cliente_id
    agendamento.cachorro_id = dados.cachorro_id
    agendamento.plano_id = dados.plano_id

    db.commit()
    db.refresh(agendamento)
    return agendamento


@router.patch("/{agendamento_id}/status", response_model=schemas.AgendamentoOut)
def atualizar_status(agendamento_id: int, dados: schemas.StatusUpdate, db: Session = Depends(get_db)):
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    agendamento.status = dados.status
    db.commit()
    db.refresh(agendamento)
    return agendamento


@router.put("/{agendamento_id}/anotacoes", response_model=schemas.AgendamentoOut)
def atualizar_anotacoes(agendamento_id: int, dados: schemas.AnotacoesUpdate, db: Session = Depends(get_db)):
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    # Importante: este endpoint funciona independentemente do status da sessão.
    # Mesmo uma aula já "Concluída" pode ter suas anotações editadas depois.
    agendamento.anotacoes = dados.anotacoes
    db.commit()
    db.refresh(agendamento)
    return agendamento


@router.delete("/{agendamento_id}", status_code=204)
def excluir_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    db.delete(agendamento)
    db.commit()
    return None

