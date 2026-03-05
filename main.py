from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.scan import router as scan_router

# Carrega as variáveis de ambiente (.env)
load_dotenv()

app = FastAPI(
    title="Cloud Optimizer SaaS",
    description="API Modular para análise de custos no GCP",
    version="0.2.0"
)

# Adicionamos as rotas que criamos no passo 2
app.include_router(scan_router)

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Cloud Optimizer estruturado e rodando!"
    }