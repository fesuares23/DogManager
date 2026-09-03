from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/cachorros", tags=["Cachorros"])


@router.get("/", response_model=list[schemas.CachorroOut])
def listar_cachorros(db: Session = Depends(get_db)):
    return db.query(models.Cachorro).all()


@router.get("/{cachorro_id}", response_model=schemas.CachorroOut)
def obter_cachorro(cachorro_id: int, db: Session = Depends(get_db)):
    cachorro = db.query(models.Cachorro).filter(models.Cachorro.id == cachorro_id).first()
    if not cachorro:
        raise HTTPException(status_code=404, detail="Cachorro não encontrado")
    return cachorro


@router.post("/", response_model=schemas.CachorroOut, status_code=201)
def criar_cachorro(dados: schemas.CachorroCreate, db: Session = Depends(get_db)):
    # Verifica se o cliente informado realmente existe antes de criar o cachorro
    cliente = db.query(models.Cliente).filter(models.Cliente.id == dados.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente informado não existe")

    novo_cachorro = models.Cachorro(**dados.model_dump())
    db.add(novo_cachorro)
    db.commit()
    db.refresh(novo_cachorro)
    return novo_cachorro


@router.put("/{cachorro_id}", response_model=schemas.CachorroOut)
def atualizar_cachorro(cachorro_id: int, dados: schemas.CachorroCreate, db: Session = Depends(get_db)):
    cachorro = db.query(models.Cachorro).filter(models.Cachorro.id == cachorro_id).first()
    if not cachorro:
        raise HTTPException(status_code=404, detail="Cachorro não encontrado")

    cliente = db.query(models.Cliente).filter(models.Cliente.id == dados.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente informado não existe")

    cachorro.nome = dados.nome
    cachorro.raca = dados.raca
    cachorro.idade = dados.idade
    cachorro.sexo = dados.sexo
    cachorro.cliente_id = dados.cliente_id

    db.commit()
    db.refresh(cachorro)
    return cachorro


@router.delete("/{cachorro_id}", status_code=204)
def excluir_cachorro(cachorro_id: int, db: Session = Depends(get_db)):
    cachorro = db.query(models.Cachorro).filter(models.Cachorro.id == cachorro_id).first()
    if not cachorro:
        raise HTTPException(status_code=404, detail="Cachorro não encontrado")

    em_uso = db.query(models.Agendamento).filter(models.Agendamento.cachorro_id == cachorro_id).first()
    if em_uso:
        raise HTTPException(
            status_code=409,
            detail="Este cachorro está vinculado a pelo menos um agendamento e não pode ser excluído.",
        )

    db.delete(cachorro)
    db.commit()
    return None
