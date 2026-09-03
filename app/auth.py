import hashlib
import os

from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session
from app import models

from dotenv import load_dotenv

load_dotenv()

USUARIO_INICIAL = os.getenv("DOGMANAGER_USUARIO")
SENHA_INICIAL = os.getenv("DOGMANAGER_SENHA_INICIAL")


def gerar_salt() -> str:
    return os.urandom(16).hex()


def criar_hash(senha: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(salt), 100_000).hex()


def obter_credencial(db: Session) -> models.Credencial | None:
    return db.query(models.Credencial).first()


def verificar_credenciais(usuario: str, senha: str, db: Session) -> bool:
    credencial = obter_credencial(db)
    if not credencial or usuario != credencial.usuario:
        return False
    return criar_hash(senha, credencial.salt) == credencial.senha_hash


def verificar_senha_atual(senha: str, db: Session) -> bool:
    credencial = obter_credencial(db)
    if not credencial:
        return False
    return criar_hash(senha, credencial.salt) == credencial.senha_hash


def atualizar_senha(nova_senha: str, db: Session) -> None:
    credencial = obter_credencial(db)
    novo_salt = gerar_salt()
    credencial.salt = novo_salt
    credencial.senha_hash = criar_hash(nova_senha, novo_salt)
    db.commit()


def exigir_login(request: Request):
    if not request.session.get("logado"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")

    