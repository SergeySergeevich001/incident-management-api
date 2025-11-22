# app/crud/incidents.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models.incident import Incident, StatusEnum
from app.schemas.incident import IncidentCreate, IncidentUpdate


def get_incident(db: Session, incident_id: int) -> Optional[Incident]:
    """Получить инцидент по ID"""
    return db.get(Incident, incident_id)


def get_incidents(
        db: Session,
        status: Optional[StatusEnum] = None,
        skip: int = 0,
        limit: int = 100
) -> List[Incident]:
    """Получить список инцидентов с фильтром по статусу"""
    query = select(Incident)

    if status:
        query = query.where(Incident.status == status)

    query = query.offset(skip).limit(limit)

    return list(db.scalars(query).all())


def create_incident(db: Session, incident: IncidentCreate) -> Incident:
    """Создать новый инцидент"""
    db_incident = Incident(
        description=incident.description,
        source=incident.source,
        status=StatusEnum.new  # По умолчанию новый
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


def update_incident_status(
        db: Session,
        incident_id: int,
        incident_update: IncidentUpdate
) -> Optional[Incident]:
    """Обновить статус инцидента"""
    db_incident = get_incident(db, incident_id)
    if not db_incident:
        return None

    db_incident.status = incident_update.status
    db.commit()
    db.refresh(db_incident)
    return db_incident


def get_incidents_count(db: Session, status: Optional[StatusEnum] = None) -> int:
    """Получить количество инцидентов (для пагинации)"""
    query = db.query(Incident)

    if status:
        query = query.filter(Incident.status == status)

    return query.count()