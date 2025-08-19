from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(
        title=task.title, description=task.description, status=task.status.value
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: str) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    return db.query(Task).offset(skip).limit(limit).all()


def update_task(db: Session, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)
    if "status" in update_data:
        update_data["status"] = update_data["status"].value

    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: str) -> bool:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True
