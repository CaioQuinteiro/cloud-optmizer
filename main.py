from fastapi import FastAPI

# Inicializa a nossa aplicação
app = FastAPI(
    title="Cloud Optimizer SaaS",
    description="API para análise e redução de custos no GCP",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Motor do Cloud Optimizer rodando perfeitamente!",
        "gcp_connected": False # Vamos mudar isso em breve
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}