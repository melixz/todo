from enum import Enum
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def generate_uuid():
    return str(uuid4())


class TaskStatus(str, Enum):
    CREATED = "создано"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default=TaskStatus.CREATED.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
