from sqlmodel import Field, Relationship
from .base import BaseModel, TODO_SCHEMA
from pydantic import EmailStr


class User(BaseModel, table=True):
    __tablename__ = "user"
    __table_args__ = {"schema": TODO_SCHEMA}
    
    first_name: str
    last_name: str
    email: EmailStr = Field(unique=True, index=True)
    user_name: str = Field(unique=True, index=True)
    password: str
    is_active: bool = Field(default=True)
    is_email_verified: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    
    tasks: list["Task"] = Relationship(
    back_populates="user",
    sa_relationship_kwargs={"lazy": "selectin"}
    )    
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}".strip()