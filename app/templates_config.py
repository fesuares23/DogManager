from fastapi.templating import Jinja2Templates

# Instância única, compartilhada por todas as rotas que precisam
# renderizar páginas HTML.
templates = Jinja2Templates(directory="app/templates")
