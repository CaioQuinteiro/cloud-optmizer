from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from app.core.database import Base

class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    projeto = Column(String, index=True)
    zona = Column(String)
    economia_estimada = Column(Float)
    vms_ociosas = Column(Integer)
    discos_ociosos = Column(Integer)
    sql_ociosos = Column(Integer, default=0)
    data_scan = Column(DateTime, default=lambda: datetime.now(timezone.utc))