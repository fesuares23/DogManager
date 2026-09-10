# 🐶 DogManager

Sistema de gestão para adestradores de cães, desenvolvido com Python e FastAPI.

O DogManager permite organizar clientes, cachorros, fichas de avaliação, planos de treinamento e agendamentos em um único sistema.


## 🚀 Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Psycopg
- Jinja2
- HTML
- CSS
- JavaScript
- Git e GitHub
- Render
- Neon


## ✨ Funcionalidades

- Cadastro e gerenciamento de clientes
- Cadastro e gerenciamento de cachorros
- Fichas de avaliação comportamental
- Cadastro de planos de treinamento
- Agendamento de aulas
- Sistema de login e autenticação
- Alteração de senha
- Persistência de dados com PostgreSQL
- Aplicação hospedada na nuvem

## 🌐 Demonstração

A aplicação está disponível online:

https://dogmanager.onrender.com


## 💻 Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/fesuares23/DogManager.git
cd DogManager


2. Crie o ambiente virtual

No Windows:

python -m venv .venv
3. Ative o ambiente virtual
.venv\Scripts\activate
4. Instale as dependências
pip install -r requirements.txt
5. Configure as variáveis de ambiente

Crie um arquivo .env na raiz do projeto e configure as variáveis necessárias para a aplicação.

O arquivo .env não deve ser enviado para o GitHub.

6. Inicie a aplicação
uvicorn app.main:app --reload

Depois, acesse:

http://127.0.0.1:8000

🗂️ Estrutura do projeto
DogManager/
├── app/
│   ├── routers/
│   ├── static/
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   ├── templates/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   └── models.py
├── .gitignore
├── requirements.txt
└── README.md


🚀 Deploy

A aplicação está hospedada utilizando:

Render — hospedagem da aplicação FastAPI
Neon — banco de dados PostgreSQL
📌 Status do projeto

Projeto funcional e hospedado online, desenvolvido como projeto de estudo e portfólio.

O projeto continua em desenvolvimento e pode receber novas funcionalidades no futuro.
