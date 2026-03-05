from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# O SQLite vai criar este arquivo na raiz do seu projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./cloud_optimizer.db"

# Se fosse PostgreSQL no futuro, seria algo como:
# SQLALCHEMY_DATABASE_URL = "postgresql://usuario:senha@localhost/nome_do_banco"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Necessário apenas para o SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A classe Base que nossos modelos vão herdar (como o @Entity do Java)
Base = declarative_base()

# Função injetável para abrir a conexão apenas quando uma rota for chamada
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()