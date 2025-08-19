from typing import List
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db, engine
from app.models import Base
from app.crud import create_task, get_task, get_tasks, update_task, delete_task
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

app = FastAPI(
    title="Task Manager API",
    description="CRUD API для управления задачами с поддержкой статусов: создано, в работе, завершено",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event():
    """Создание таблиц при запуске приложения."""
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Task Manager API"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


@app.post(
    "/tasks/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
)
async def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)


@app.get("/tasks/", response_model=List[TaskResponse], tags=["Tasks"])
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_tasks(db=db, skip=skip, limit=limit)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def read_task(task_id: str, db: Session = Depends(get_db)):
    task = get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
async def update_existing_task(
    task_id: str, task_update: TaskUpdate, db: Session = Depends(get_db)
):
    task = update_task(db=db, task_id=task_id, task_update=task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_existing_task(task_id: str, db: Session = Depends(get_db)):
    if not delete_task(db=db, task_id=task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
