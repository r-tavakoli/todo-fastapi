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