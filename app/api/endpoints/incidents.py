# app/api/endpoints/incidents.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.incident import (
    Incident, IncidentCreate, IncidentUpdate, IncidentList, StatusEnum
)
from app.crud import incidents as crud

router = APIRouter()


@router.post(
    "/",
    response_model=Incident,
    status_code=status.HTTP_201_CREATED,
    summary="Создать инцидент",
    description="Создает новый инцидент с статусом 'new'"
)
def create_incident(
        incident: IncidentCreate,
        db: Session = Depends(get_db)
) -> Incident:
    """Создать новый инцидент"""
    return crud.create_incident(db=db, incident=incident)


@router.get(
    "/",
    response_model=IncidentList,
    summary="Получить список инцидентов",
    description="Возвращает список инцидентов с возможностью фильтрации по статусу"
)
def get_incidents(
        status: Optional[StatusEnum] = Query(None, description="Фильтр по статусу"),
        skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
        limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
        db: Session = Depends(get_db)
) -> IncidentList:
    """Получить список инцидентов с фильтрацией"""
    incidents = crud.get_incidents(db=db, status=status, skip=skip, limit=limit)
    total = crud.get_incidents_count(db=db, status=status)

    return IncidentList(incidents=incidents, total=total)


@router.patch(
    "/{incident_id}",
    response_model=Incident,
    summary="Обновить статус инцидента",
    description="Обновляет статус инцидента по ID. Возвращает 404 если инцидент не найден"
)
def update_incident_status(
        incident_id: int,
        incident_update: IncidentUpdate,
        db: Session = Depends(get_db)
) -> Incident:
    """Обновить статус инцидента"""
    db_incident = crud.update_incident_status(
        db=db,
        incident_id=incident_id,
        incident_update=incident_update
    )

    if db_incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Инцидент с ID {incident_id} не найден"
        )

    return db_incident


@router.get(
    "/{incident_id}",
    response_model=Incident,
    summary="Получить инцидент по ID",
    description="Возвращает инцидент по его ID. Возвращает 404 если не найден"
)
def get_incident(
        incident_id: int,
        db: Session = Depends(get_db)
) -> Incident:
    """Получить инцидент по ID"""
    db_incident = crud.get_incident(db=db, incident_id=incident_id)

    if db_incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Инцидент с ID {incident_id} не найден"
        )

    return db_incident