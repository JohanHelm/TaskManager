import enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StatusEnum(enum.Enum):
    created = "created"
    in_progress = "in progress"
    completed = "completed"


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(TaskBase):
    name: str
    description: str
    status: StatusEnum


class TaskFromDB(TaskCreate):
    id: UUID


class TaskUpdate(TaskBase):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
