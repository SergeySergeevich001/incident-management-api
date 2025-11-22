# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import create_tables
from app.models.incident import Base
from app.api.endpoints import incidents


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan manager для создания таблиц при запуске"""
    # Создаем таблицы при запуске приложения
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")
    yield
    # При завершении работы можно добавить cleanup логику
    print("Shutting down...")

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Incident Management API",
    description="API для учёта инцидентов - тестовое задание для UCAR/TOPDOER",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Подключаем роутер инцидентов
app.include_router(
    incidents.router,
    prefix="/incidents",
    tags=["incidents"]
)

@app.get("/")
async def root():
    """Корневой эндпоинт с информацией о API"""
    return {
        "message": "Incident Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "create_incident": "POST /incidents/",
            "get_incidents": "GET /incidents/",
            "update_incident": "PATCH /incidents/{id}",
            "get_incident": "GET /incidents/{id}"
        }
    }

@app.get("/health")
async def health_check():
    """Health check эндпоинт для мониторинга"""
    return {"status": "healthy", "service": "incident-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )