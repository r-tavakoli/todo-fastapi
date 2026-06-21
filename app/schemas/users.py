from pydantic import BaseModel, Field
from pydantic import EmailStr
from .base import CreateResponse, UpdateResponse, DeleteResponse

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