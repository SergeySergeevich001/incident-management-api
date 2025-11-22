import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models.incident import Base

# Тестовая база данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_incidents.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределяем dependency для тестов"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Фикстура для создания и очистки тестовой БД"""
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    yield
    # Удаляем таблицы после теста
    Base.metadata.drop_all(bind=engine)


def test_create_incident(test_db):
    """Тест создания инцидента"""
    response = client.post(
        "/incidents/",
        json={
            "description": "Самокат не в сети",
            "source": "operator"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Самокат не в сети"
    assert data["source"] == "operator"
    assert data["status"] == "new"
    assert "id" in data
    assert "created_at" in data


def test_get_incidents_empty(test_db):
    """Тест получения пустого списка инцидентов"""
    response = client.get("/incidents/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["incidents"] == []


def test_get_incidents_with_data(test_db):
    """Тест получения списка с данными"""
    # Создаем инцидент
    client.post("/incidents/", json={
        "description": "Тест 1",
        "source": "monitoring"
    })

    response = client.get("/incidents/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["incidents"]) == 1
    assert data["incidents"][0]["description"] == "Тест 1"


def test_get_incidents_filter_by_status(test_db):
    """Тест фильтрации по статусу"""
    # Создаем несколько инцидентов
    client.post("/incidents/", json={"description": "Новый", "source": "operator"})

    response = client.get("/incidents/?status=new")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    for incident in data["incidents"]:
        assert incident["status"] == "new"


def test_update_incident_status(test_db):
    """Тест обновления статуса инцидента"""
    # Создаем инцидент
    create_response = client.post("/incidents/", json={
        "description": "Для обновления",
        "source": "partner"
    })
    incident_id = create_response.json()["id"]

    # Обновляем статус
    update_response = client.patch(
        f"/incidents/{incident_id}",
        json={"status": "in_progress"}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["status"] == "in_progress"
    assert data["id"] == incident_id


def test_update_nonexistent_incident(test_db):
    """Тест обновления несуществующего инцидента"""
    response = client.patch(
        "/incidents/999",
        json={"status": "resolved"}
    )
    assert response.status_code == 404
    assert "не найден" in response.json()["detail"]


def test_get_incident_by_id(test_db):
    """Тест получения инцидента по ID"""
    create_response = client.post("/incidents/", json={
        "description": "Для получения",
        "source": "monitoring"
    })
    incident_id = create_response.json()["id"]

    response = client.get(f"/incidents/{incident_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == incident_id
    assert data["description"] == "Для получения"


def test_get_nonexistent_incident(test_db):
    """Тест получения несуществующего инцидента"""
    response = client.get("/incidents/999")
    assert response.status_code == 404


def test_root_endpoint(test_db):
    """Тест корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data


def test_health_check(test_db):
    """Тест health check эндпоинта"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"