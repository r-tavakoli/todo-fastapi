from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import CreateResponse, UpdateResponse, DeleteResponse


class BaseTask(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    status_id: int
    priority_id: int
    due_date_time: datetime
        
class ReadTaskResponse(BaseTask):
    is_deleted: bool
    created_on: datetime
    modified_on: datetime

class CreateTask(BaseTask):
    pass

class CreateTaskResponse(CreateResponse):
    pass
    
class UpdateTask(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    status_id: Optional[int] = None
    priority_id: Optional[int] = None
    due_date_time: Optional[datetime] = None
    
class UpdateTaskResponse(UpdateResponse):
    pass

class DeleteTaskResponse(DeleteResponse):
    pass
