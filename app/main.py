import os

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.database import Base, engine, SessionLocal
from app import models
from app.auth import exigir_login, gerar_salt, criar_hash, USUARIO_INICIAL, SENHA_INICIAL
from app.routers import paginas, clientes, cachorros, avaliacoes, planos, agenda

load_dotenv()

app = FastAPI(title="Sistema de Gestão - Adestrador de Cães")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("DOGMANAGER_SECRET_KEY"))

app.mount("/static", StaticFiles(directory="app/static"), name="static")

Base.metadata.create_all(bind=engine)

def seed_credencial_inicial():
    
    db = SessionLocal()
    try:
        if not db.query(models.Credencial).first():
            salt = gerar_salt()
            credencial = models.Credencial(
                usuario=USUARIO_INICIAL,
                senha_hash=criar_hash(SENHA_INICIAL, salt),
                salt=salt,
            )
            db.add(credencial)
            db.commit()
    finally:
        db.close()


seed_credencial_inicial()

app.include_router(paginas.router)

app.include_router(clientes.router, prefix="/api", dependencies=[Depends(exigir_login)])
app.include_router(cachorros.router, prefix="/api", dependencies=[Depends(exigir_login)])
app.include_router(avaliacoes.router, prefix="/api", dependencies=[Depends(exigir_login)])
app.include_router(planos.router, prefix="/api", dependencies=[Depends(exigir_login)])
app.include_router(agenda.router, prefix="/api", dependencies=[Depends(exigir_login)])
