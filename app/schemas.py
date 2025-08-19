from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, field_serializer
from app.models import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime

    @field_serializer("id")
    def serialize_id(self, value: Any) -> str:
        return str(value)

    class Config:
        from_attributes = True
