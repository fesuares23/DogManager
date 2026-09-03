from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/planos", tags=["Planos"])


@router.get("/", response_model=list[schemas.PlanoOut])
def listar_planos(db: Session = Depends(get_db)):
    return db.query(models.Plano).all()


@router.get("/{plano_id}", response_model=schemas.PlanoOut)
def obter_plano(plano_id: int, db: Session = Depends(get_db)):
    plano = db.query(models.Plano).filter(models.Plano.id == plano_id).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    return plano


@router.post("/", response_model=schemas.PlanoOut, status_code=201)
def criar_plano(dados: schemas.PlanoCreate, db: Session = Depends(get_db)):
    novo_plano = models.Plano(**dados.model_dump())
    db.add(novo_plano)
    db.commit()
    db.refresh(novo_plano)
    return novo_plano


@router.put("/{plano_id}", response_model=schemas.PlanoOut)
def atualizar_plano(plano_id: int, dados: schemas.PlanoCreate, db: Session = Depends(get_db)):
    plano = db.query(models.Plano).filter(models.Plano.id == plano_id).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    plano.nome = dados.nome
    plano.quantidade_sessoes = dados.quantidade_sessoes

    db.commit()
    db.refresh(plano)
    return plano


@router.delete("/{plano_id}", status_code=204)
def excluir_plano(plano_id: int, db: Session = Depends(get_db)):
    plano = db.query(models.Plano).filter(models.Plano.id == plano_id).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    em_uso = db.query(models.Agendamento).filter(models.Agendamento.plano_id == plano_id).first()
    if em_uso:
        raise HTTPException(
            status_code=409,
            detail="Este plano está sendo usado em pelo menos um agendamento e não pode ser excluído.",
        )

    db.delete(plano)
    db.commit()
    return None
