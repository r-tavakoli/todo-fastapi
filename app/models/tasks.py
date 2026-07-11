from typing import List
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from .base import BaseModel, TODO_SCHEMA


class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tag"
    __table_args__ = {"schema": TODO_SCHEMA}
    
    task_id: int = Field(foreign_key=f"{TODO_SCHEMA}.task.id", primary_key=True)
    tag_id: int = Field(foreign_key=f"{TODO_SCHEMA}.tag.id", primary_key=True)


class Task(BaseModel, table=True):
    __tablename__ = "task"
    __table_args__ = {"schema": TODO_SCHEMA}
    
    title: str = Field(max_length=100, min_length=3)
    status_id: int = Field(foreign_key=f"{TODO_SCHEMA}.status.id", default=1)
    priority_id: int = Field(foreign_key=f"{TODO_SCHEMA}.priority.id", default=1)
    due_date_time: datetime
    tags: List["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTag,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    is_deleted: bool = Field(default=False)
    user_id: int = Field(foreign_key=f"{TODO_SCHEMA}.user.id")
    
    user: "User" = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    

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
    
class Tag(BaseModel, table=True):
    __tablename__ = "tag"
    __table_args__ = {"schema": TODO_SCHEMA}
    
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=50)
    is_deleted: bool = Field(default=False)
    
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTag)
    