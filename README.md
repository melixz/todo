# todo
CRUD-сервис для управления задачами (uuid, название, описание, статусы: создано, в работе, завершено) на FastAPI с Pydantic и SQLAlchemy (SQLite).

## Особенности

- **Полный CRUD**: create, get, list, update, delete
- **Схемы**: Pydantic-модели с валидацией
- **Хранилище**: SQLite через SQLAlchemy
- **Тесты**: Gauge
- **Swagger-документация**: краткие описания и примеры запросов/ответов
- **Docker**: готовая контейнеризация

## Быстрый старт

### Требования

- Python 3.11+
- uv (пакетный менеджер)
- Docker (опционально)

### Установка

1. Установите [uv](https://github.com/astral-sh/uv):
```bash
# На Linux/macOS через curl
curl -LsSf https://astral.sh/uv/install.sh | sh
# или через pip
pip install uv
```

2. Установите зависимости:
```bash
uv sync
```

3. Запустите приложение:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Откройте Swagger UI: http://localhost:8000/docs

## Docker запуск

### Быстрый старт с Docker
```bash
docker-compose up --build
```
Приложение будет доступно по адресу: `http://localhost:8000`

## Структура проекта

```
.
├── app/
│   ├── main.py               # Точка входа FastAPI; подключение роутеров
│   ├── api/
│   │   ├── tasks.py          # Роутер CRUD для задач 
│   │   └── crud.py           # CRUD-логика 
│   ├── core/
│   │   ├── database.py       # Подключение к БД и сессии 
│   │   ├── models.py         # SQLAlchemy модели
│   │   └── schemas.py        # Pydantic-схемы
├── tests/                    # Тесты
├── Dockerfile                # Контейнеризация
├── docker-compose.yml        # Локальный запуск
├── pyproject.toml            # Зависимости проекта
├── .env.example              # Пример конфигурации
└── README.md
```

## API

- `POST /tasks/` — создать задачу
- `GET /tasks/` — список задач (параметры: `skip`, `limit`)
- `GET /tasks/{task_id}` — получить задачу
- `PUT /tasks/{task_id}` — обновить задачу
- `DELETE /tasks/{task_id}` — удалить задачу

## Тестирование

### Запуск тестов
```bash
# Запустите API
# Предварительно скачайте себе gauge 
# Не забудьте перейти по пути /todo/tests 
#Выполните команду
gauge run specs
```