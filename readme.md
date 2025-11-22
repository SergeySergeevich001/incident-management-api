# Кейс-задание

---

**Задача**

Сделать маленький API-сервис для учёта инцидентов.

**Контекст**: операторы и системы присылают сообщения о проблемах в TG (самокат не в сети, точка не отвечает, отчёт не выгрузился). Не хотим **терять это в чатах.**

---

### Требования

Технологии:

- Python

- Любой знакомый тебе веб-фреймворк (предпочитаем что-то из стека в вакансии: FastAPI/Flask/Django)

- Любое простое персистентное хранилище (SQLite/Postgres/MySQL и тп)

Функциональность:

Инцидент должен иметь:

- id

- текст/описание

- статус (любой вменяемый набор, не 0/1)

- источник (например, operator / monitoring / partner)

- время создания



Нужны 3 вещи:

1. **Создать инцидент**

2. **Получить список инцидентов (с фильтром по статусу)**

3. **Обновить статус инцидента по id**
Если не найден — вернуть 404.



# Incident Management API (документация)

API сервис для учёта инцидентов. Тестовое задание для UCAR/TOPDOER.

## Технологии

- Python 3.8+
- FastAPI
- SQLAlchemy  
- SQLite
- Pydantic

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd incident-management-api
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите приложение:
```bash
python run.py
```

4. Откройте в браузере:
- **Swagger UI**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/

## Основные эндпоинты

### Создать инцидент
```http
POST /incidents/
Content-Type: application/json

{
  "description": "Самокат не в сети",
  "source": "operator"
}
```

### Получить список инцидентов
```http
GET /incidents/
GET /incidents/?status=new
GET /incidents/?status=in_progress&skip=0&limit=10
```

### Обновить статус инцидента
```http
PATCH /incidents/1
Content-Type: application/json

{
  "status": "in_progress"
}
```

### Получить инцидент по ID
```http
GET /incidents/1
```

### Корневой эндпоинт
```http
GET /
```

### Health Check
```http
GET /health
```

## Модель данных

Инцедент имеет:
- `id` - уникальный идентификатор (автоинкремент)
- `description` - описание проблемы (обязательное)
- `status` - статус: `new`, `in_progress`, `resolved`, `closed`
- `source` - источник: `operator`, `monitoring`, `partner` 
- `created_at` - время создания (автоматически)

## Примеры использования

### Создание инцидента
```bash
curl -X POST "http://localhost:8000/incidents/" \
-H "Content-Type: application/json" \
-d '{"description": "Точка не отвечает", "source": "monitoring"}'
```

### Получение списка
```bash
curl "http://localhost:8000/incidents/?status=new"
```

### Обновление статуса
```bash
curl -X PATCH "http://localhost:8000/incidents/1" \
-H "Content-Type: application/json" \
-d '{"status": "resolved"}'
```

### Получение по ID
```bash
curl "http://localhost:8000/incidents/1"
```

## Тестирование

Запустите тесты:
```bash
pytest tests/
```

## Структура проекта
```
app/
├── models/          # SQLAlchemy модели
├── schemas/         # Pydantic схемы
├── crud/           # Бизнес-логика
├── api/            # Эндпоинты FastAPI
└── database.py     # Настройка БД
```

**Примечание**: При первом запуске автоматически создается SQLite база данных `incidents.db` и таблицы.