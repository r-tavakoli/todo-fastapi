from sqlmodel import Field
from datetime import datetime
from .base import BaseModel, TODO_SCHEMA


class Task(BaseModel, table=True):
    __tablename__ = "task"
    __table_args__ = {"schema": TODO_SCHEMA}
    
    title: str = Field(max_length=100, min_length=3)
    status_id: int = Field(foreign_key=f"{TODO_SCHEMA}.status.id", default=1)
    priority_id: int = Field(foreign_key=f"{TODO_SCHEMA}.priority.id", default=1)
    due_date_time: datetime
    is_deleted: bool = Field(default=False)

class Status(BaseModel, table=True):
    __tablename__ = "status"
    __table_args__ = {"schema": TODO_SCHEMA}
    
    title: str = Field(max_length=50, min_length=3)
    is_deleted: bool = Field(default=False)

class Priority(BaseModel, table=True):
    __tablename__ = "priority"
    __table_args__ = {"schema": TODO_SCHEMA}

    title: str = Field(max_length=50, min_length=3)
    is_deleted: bool = Field(default=False)