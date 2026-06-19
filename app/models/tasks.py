from sqlmodel import SQLModel, Field
from sqlalchemy import text
from typing import Optional
from datetime import datetime

TODO_SCHEMA = "todo"

class BaseModel(SQLModel):
    __abstract__ = True
    
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        index=True,
        description="unique identifier"
    )
    
    created_on: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("TIMEZONE('utc', NOW())"),
            "nullable": False
        }
    )
    
    modified_on: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": text("TIMEZONE('utc', NOW())"),
            "onupdate": text("TIMEZONE('utc', NOW())"),
            "nullable": False
        }
    )
    
    class Config:
        from_attributes = True


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