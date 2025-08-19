from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine
from app.core.models import Base
from app.api.tasks import router as tasks_router

tags_metadata = [
    {"name": "Root", "description": "Информация о сервисе."},
    {"name": "Health", "description": "Проверка состояния сервиса."},
    {"name": "Tasks", "description": "Операции CRUD над задачами."},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация ресурсов приложения."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Task Manager API",
    description="CRUD API для управления задачами. Статусы: создано, в работе, завершено.",
    version="0.1.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)


@app.get(
    "/",
    tags=["Root"],
    summary="Корневой маршрут",
    description="Простое сообщение, чтобы проверить, что сервис запущен.",
)
async def root():
    return {"message": "Task Manager API"}


@app.get(
    "/health",
    tags=["Health"],
    summary="Проверка здоровья",
    description="Возвращает текущий статус приложения.",
)
async def health_check():
    return {"status": "healthy"}


@app.get("/openapi.json", include_in_schema=False)
async def openapi_spec():
    """Позволяет явно получить OpenAPI схему (удобно для тестов/линтеров)."""
    return app.openapi()


app.include_router(tasks_router)
