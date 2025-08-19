from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.crud import create_task, get_task, get_tasks, update_task, delete_task
from app.core.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
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


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Список задач",
    description="Возвращает список задач с пагинацией.",
)
async def read_tasks(
    skip: int = Query(0, ge=0, description="Сколько задач пропустить (offset)"),
    limit: int = Query(100, ge=1, le=1000, description="Максимум задач в ответе"),
    db: Session = Depends(get_db),
):
    return get_tasks(db=db, skip=skip, limit=limit)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
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


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
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


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
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
