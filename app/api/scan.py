from fastapi import APIRouter, HTTPException
from app.services.gcp.scanner import obter_vms_ociosas, obter_discos_ociosos

# Criamos um "mini-app" apenas para as rotas de scan
router = APIRouter(prefix="/api/v1/scan", tags=["GCP Scanner"])

@router.get("/idle-vms")
def scan_idle_vms(zona: str = "us-central1-a"):
    try:
        return obter_vms_ociosas(zona)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro GCP: {str(e)}")

@router.get("/idle-disks")
def scan_idle_disks(zona: str = "us-central1-a"):
    try:
        return obter_discos_ociosos(zona)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro GCP: {str(e)}")

@router.get("/full")
def scan_full(zona: str = "us-central1-a"):
    try:
        resultado_vms = obter_vms_ociosas(zona)
        resultado_discos = obter_discos_ociosos(zona)
        
        economia_geral = resultado_vms["economia_total_estimada"] + resultado_discos["economia_total_estimada"]
        
        return {
            "projeto": resultado_vms["projeto"],
            "zona": zona,
            "economia_total_estimada": economia_geral,
            "resumo": {
                "vms_ociosas": resultado_vms["oportunidades"],
                "discos_ociosos": resultado_discos["oportunidades"],
            },
            "detalhes": {
                "vms": resultado_vms["detalhes"],
                "discos": resultado_discos["detalhes"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no Scan Completo: {str(e)}")