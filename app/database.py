from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão do SQLite. O arquivo "adestrador.db" será criado
# automaticamente na raiz do projeto na primeira execução.
SQLALCHEMY_DATABASE_URL = "sqlite:///./adestrador.db"

# O "engine" é o objeto que efetivamente sabe conversar com o banco.
# connect_args é necessário apenas para SQLite, pois por padrão ele
# não permite uso por múltiplas threads (o FastAPI usa várias).
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal é uma "fábrica" de sessões. Cada requisição que chega
# na API vai abrir uma sessão nova para conversar com o banco.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base é a classe da qual todos os nossos modelos (tabelas) vão herdar.
Base = declarative_base()


def get_db():
    """
    Cria uma sessão do banco, entrega para a rota que precisa dela,
    e garante que ela seja fechada no final — mesmo se der erro.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        