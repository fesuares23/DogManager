from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=list[schemas.ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()


@router.get("/{cliente_id}", response_model=schemas.ClienteOut)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.post("/", response_model=schemas.ClienteOut, status_code=201)
def criar_cliente(dados: schemas.ClienteCreate, db: Session = Depends(get_db)):
    novo_cliente = models.Cliente(**dados.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente


@router.put("/{cliente_id}", response_model=schemas.ClienteOut)
def atualizar_cliente(cliente_id: int, dados: schemas.ClienteCreate, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    cliente.nome = dados.nome
    cliente.telefone = dados.telefone
    cliente.endereco = dados.endereco

    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}", status_code=204)
def excluir_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    ids_cachorros = [c.id for c in cliente.cachorros]

    em_uso = (
        db.query(models.Agendamento)
        .filter(
            (models.Agendamento.cliente_id == cliente_id)
            | (models.Agendamento.cachorro_id.in_(ids_cachorros))
        )
        .first()
    )
    if em_uso:
        raise HTTPException(
            status_code=409,
            detail="Este cliente (ou um cachorro dele) está vinculado a pelo menos um agendamento e não pode ser excluído.",
        )

    db.delete(cliente)
    db.commit()
    return None
