#app/models/incident.py
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class StatusEnum(enum.Enum):
    """Статусы инцидентов"""
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class SourceEnum(enum.Enum):
    """Источники инцидентов"""
    operator = "operator"
    monitoring = "monitoring" 
    partner = "partner"

class Incident(Base):
    """Модель инцидента в базе данных"""
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.new, nullable=False)
    source = Column(Enum(SourceEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Incident(id={self.id}, status='{self.status.value}', source='{self.source.value}')>"