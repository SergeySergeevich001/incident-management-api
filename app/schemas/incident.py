#app/schemas/incident.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Optional


class StatusEnum(str, Enum):
    """Статусы инцидентов для API"""
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class SourceEnum(str, Enum):
    """Источники инцидентов для API"""
    operator = "operator"
    monitoring = "monitoring"
    partner = "partner"


class IncidentBase(BaseModel):
    """Базовая схема инцидента"""
    description: str
    source: SourceEnum


class IncidentCreate(IncidentBase):
    """Схема для создания инцидента"""
    pass


class IncidentUpdate(BaseModel):
    """Схема для обновления инцидента"""
    status: StatusEnum


class Incident(IncidentBase):
    """Схема для возврата инцидента"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: StatusEnum
    created_at: datetime


class IncidentList(BaseModel):
    """Схема для списка инцидентов"""
    incidents: list[Incident]
    total: int