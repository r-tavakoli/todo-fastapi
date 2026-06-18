from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
class Status(str, Enum):
    IN_PORGRESS = "in_progress"
    COMPLETED = "completed"
    BACK_LOG = "back_log"
    CANCELED = "canceled"

class BaseTask(BaseModel):
    task_id: int
    priority: Priority.MEDIUM
    status: Status.BACK_LOG
    due_date: datetime
        
        
class ReadTask(BaseTask):
    pass

class CreateTask(BaseTask):
    pass

class DeleteTask(BaseTask):
    pass
