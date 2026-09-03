from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/cachorros", tags=["Ficha de Avaliação"])


@router.get("/{cachorro_id}/ficha", response_model=schemas.FichaAvaliacaoOut)
def obter_ficha(cachorro_id: int, db: Session = Depends(get_db)):
    cachorro = db.query(models.Cachorro).filter(models.Cachorro.id == cachorro_id).first()
    if not cachorro:
        raise HTTPException(status_code=404, detail="Cachorro não encontrado")

    if not cachorro.ficha_avaliacao:
        raise HTTPException(status_code=404, detail="Ficha de avaliação ainda não foi criada para este cachorro")

    return cachorro.ficha_avaliacao


@router.put("/{cachorro_id}/ficha", response_model=schemas.FichaAvaliacaoOut)
def criar_ou_atualizar_ficha(cachorro_id: int, dados: schemas.FichaAvaliacaoCreate, db: Session = Depends(get_db)):
    cachorro = db.query(models.Cachorro).filter(models.Cachorro.id == cachorro_id).first()
    if not cachorro:
        raise HTTPException(status_code=404, detail="Cachorro não encontrado")

    ficha = cachorro.ficha_avaliacao

    if ficha:
        # A ficha já existe: apenas atualiza os campos
        ficha.queixa_principal = dados.queixa_principal
        ficha.historico_comportamento = dados.historico_comportamento
        ficha.expectativa_dono = dados.expectativa_dono
    else:
        # Ainda não existe: cria uma nova, já vinculada a este cachorro
        ficha = models.FichaAvaliacao(cachorro_id=cachorro_id, **dados.model_dump())
        db.add(ficha)

    db.commit()
    db.refresh(ficha)
    return ficha
