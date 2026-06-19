from pydantic import BaseModel, Field
from datetime import datetime


class BaseTask(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    status_id: int
    priority_id: int
    due_date_time: datetime
        
class ReadTask(BaseTask):
    is_deleted: bool
    created_on: datetime
    modified_on: datetime

class CreateTask(BaseTask):
    pass

class CreateeTaskResponse(BaseModel):
    id: int
    message: str = "created successfully"

class DeleteTask(BaseTask):
    pass
