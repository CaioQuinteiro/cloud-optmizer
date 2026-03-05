from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.gcp.scanner import obter_vms_ociosas, obter_discos_ociosos, obter_sql_ociosos
from app.core.database import get_db
from app.models.scan import ScanHistory

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

@router.get("/idle-sql")
def scan_idle_sql(zona: str = "us-central1-a"):
    try:
        return obter_sql_ociosos(zona)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro GCP: {str(e)}")

@router.get("/full")
def scan_full(zona: str = "us-central1-a", db: Session = Depends(get_db)):
    try:
        resultado_vms = obter_vms_ociosas(zona)
        resultado_discos = obter_discos_ociosos(zona)
        resultado_sql = obter_sql_ociosos(zona) # <-- Novo scanner chamado!
        
        # Somamos a economia total das 3 fontes
        economia_geral = (
            resultado_vms["economia_total_estimada"] + 
            resultado_discos["economia_total_estimada"] +
            resultado_sql["economia_total_estimada"]
        )
        
        novo_scan = ScanHistory(
            projeto=resultado_vms["projeto"],
            zona=zona,
            economia_estimada=economia_geral,
            vms_ociosas=resultado_vms["oportunidades"],
            discos_ociosos=resultado_discos["oportunidades"],
            sql_ociosos=resultado_sql["oportunidades"] # <-- Salvando no banco
        )
        
        db.add(novo_scan)
        db.commit()
        db.refresh(novo_scan)
        
        return {
            "scan_id": novo_scan.id,
            "projeto": resultado_vms["projeto"],
            "zona": zona,
            "economia_total_estimada": economia_geral,
            "resumo": {
                "vms_ociosas": resultado_vms["oportunidades"],
                "discos_ociosos": resultado_discos["oportunidades"],
                "sql_ociosos": resultado_sql["oportunidades"],
                "total_oportunidades": (
                    resultado_vms["oportunidades"] + 
                    resultado_discos["oportunidades"] + 
                    resultado_sql["oportunidades"]
                )
            },
            "detalhes": {
                "vms": resultado_vms["detalhes"],
                "discos": resultado_discos["detalhes"],
                "sql": resultado_sql["detalhes"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no Scan Completo: {str(e)}")

@router.get("/history")
def get_scan_history(limit: int = 10, db: Session = Depends(get_db)):
    """
    Retorna o histórico das últimas varreduras, do mais recente para o mais antigo.
    """
    try:
        # Fazemos um SELECT na tabela, ordenando pelo ID (decrescente) e limitando a quantidade
        historico = db.query(ScanHistory).order_by(ScanHistory.id.desc()).limit(limit).all()
        return {
            "total_registros_retornados": len(historico),
            "historico": historico
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")