from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.templates_config import templates
from app.auth import verificar_credenciais, verificar_senha_atual, atualizar_senha

router = APIRouter(tags=["Páginas"])


def _exigir_login_pagina(request: Request):
    if not request.session.get("logado"):
        return RedirectResponse(url="/login")
    return None


@router.get("/")
def raiz(request: Request):
    if request.session.get("logado"):
        return RedirectResponse(url="/dashboard")
    return RedirectResponse(url="/login")


@router.get("/login")
def pagina_login(request: Request):
    return templates.TemplateResponse(request, "login.html", {"erro": None})


@router.post("/login")
def processar_login(
    request: Request, usuario: str = Form(...), senha: str = Form(...), db: Session = Depends(get_db)
):
    if verificar_credenciais(usuario, senha, db):
        request.session["logado"] = True
        return RedirectResponse(url="/dashboard", status_code=303)

    return templates.TemplateResponse(
        request, "login.html", {"erro": "Usuário ou senha inválidos"}, status_code=401
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")


@router.get("/dashboard")
def dashboard(request: Request):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento
    return templates.TemplateResponse(request, "dashboard.html", {})


@router.get("/clientes")
def pagina_clientes(request: Request):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento
    return templates.TemplateResponse(request, "clientes.html", {})


@router.get("/cachorros")
def pagina_cachorros(request: Request):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento
    return templates.TemplateResponse(request, "cachorros.html", {})


@router.get("/cachorros/{cachorro_id}/ficha")
def pagina_ficha_avaliacao(cachorro_id: int, request: Request):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento
    return templates.TemplateResponse(request, "ficha.html", {"cachorro_id": cachorro_id})


@router.get("/planos")
def pagina_planos(request: Request):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento
    return templates.TemplateResponse(request, "planos.html", {})


@router.get("/agenda")
def pagina_agenda(request: Request):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento
    return templates.TemplateResponse(request, "agenda.html", {})


@router.get("/agenda")
def pagina_agenda(request: Request):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento
    return templates.TemplateResponse(request, "agenda.html", {})


@router.get("/agenda/{agendamento_id}/anotacoes")
def pagina_anotacoes(agendamento_id: int, request: Request):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento
    return templates.TemplateResponse(request, "anotacoes.html", {"agendamento_id": agendamento_id})


@router.get("/trocar-senha")
def pagina_trocar_senha(request: Request):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento
    return templates.TemplateResponse(request, "trocar_senha.html", {"erro": None, "sucesso": None})


@router.post("/trocar-senha")
def processar_trocar_senha(
    request: Request,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    confirmar_senha: str = Form(...),
    db: Session = Depends(get_db),
):
    redirecionamento = _exigir_login_pagina(request)
    if redirecionamento:
        return redirecionamento

    if not verificar_senha_atual(senha_atual, db):
        return templates.TemplateResponse(
            request, "trocar_senha.html",
            {"erro": "Senha atual incorreta.", "sucesso": None},
            status_code=401,
        )

    if nova_senha != confirmar_senha:
        return templates.TemplateResponse(
            request, "trocar_senha.html",
            {"erro": "A nova senha e a confirmação não coincidem.", "sucesso": None},
            status_code=400,
        )

    atualizar_senha(nova_senha, db)

    return templates.TemplateResponse(
        request, "trocar_senha.html",
        {"erro": None, "sucesso": "Senha alterada com sucesso!"},
    )

