from pydantic import BaseModel, Field
from pydantic import EmailStr
from .base import CreateResponse
from datetime import datetime

class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_name: str
    password: str
        
class ReadUser(BaseUser):
    pass

class CreateUser(BaseUser):
    pass

class CreateUserResponse(CreateResponse):
    pass

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    user_name: str
    is_active: bool
    is_email_verified: bool
    created_on: datetime
    modified_on: datetime