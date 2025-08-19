from typing import List
from fastapi import FastAPI, HTTPException, Depends, status, Query, Path, Body
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.database import get_db, engine
from app.models import Base
from app.crud import create_task, get_task, get_tasks, update_task, delete_task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

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
    description="Короткая и ясная CRUD API для управления задачами. Статусы: создано, в работе, завершено.",
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


@app.post(
    "/tasks/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Создать задачу",
    description="Создаёт новую задачу по переданным данным.",
)
async def create_new_task(
    task: TaskCreate = Body(
        ...,
        examples=[
            {"summary": "Минимальные поля", "value": {"title": "Сдать отчёт"}},
            {
                "summary": "Все поля",
                "value": {
                    "title": "Обновить документацию",
                    "description": "Причесать Swagger",
                    "status": "в работе",
                },
            },
        ],
    ),
    db: Session = Depends(get_db),
):
    return create_task(db=db, task=task)


@app.get(
    "/tasks/",
    response_model=List[TaskResponse],
    tags=["Tasks"],
    summary="Список задач",
    description="Возвращает список задач с пагинацией.",
)
async def read_tasks(
    skip: int = Query(0, ge=0, description="Сколько задач пропустить (offset)"),
    limit: int = Query(100, ge=1, le=1000, description="Максимум задач в ответе"),
    db: Session = Depends(get_db),
):
    return get_tasks(db=db, skip=skip, limit=limit)


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Получить задачу",
    description="Возвращает задачу по её UUID.",
    responses={
        404: {
            "description": "Задача не найдена",
            "content": {
                "application/json": {"example": {"detail": "Задача не найдена"}}
            },
        },
    },
)
async def read_task(
    task_id: str = Path(..., description="UUID задачи"),
    db: Session = Depends(get_db),
):
    task = get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return task


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Обновить задачу",
    description="Частично или полностью обновляет поля задачи.",
    responses={
        404: {
            "description": "Задача не найдена",
            "content": {
                "application/json": {"example": {"detail": "Задача не найдена"}}
            },
        },
    },
)
async def update_existing_task(
    task_id: str = Path(..., description="UUID задачи"),
    task_update: TaskUpdate = Body(
        ...,
        examples=[
            {"summary": "Изменение статуса", "value": {"status": "завершено"}},
            {"summary": "Изменение названия", "value": {"title": "Новый заголовок"}},
        ],
    ),
    db: Session = Depends(get_db),
):
    task = update_task(db=db, task_id=task_id, task_update=task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Удалить задачу",
    description="Удаляет задачу по её UUID. В ответе тело отсутствует.",
    responses={
        404: {
            "description": "Задача не найдена",
            "content": {
                "application/json": {"example": {"detail": "Задача не найдена"}}
            },
        },
        204: {"description": "Удалено"},
    },
)
async def delete_existing_task(
    task_id: str = Path(..., description="UUID задачи"),
    db: Session = Depends(get_db),
):
    if not delete_task(db=db, task_id=task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
