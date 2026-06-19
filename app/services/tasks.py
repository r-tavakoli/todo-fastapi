from app.api.dependencies import SessionDep
from app.models.tasks import Task
from app.schemas.tasks import CreateTask

class TaskService:
    
    def __init__(self, session: SessionDep):
        self.session = session
    
    async def get(self, id: int) -> Task:
        return await self.session.get(Task, id)
    
    async def add(self, task: CreateTask) -> Task:
        new_task = Task(**task.model_dump())
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        
        return new_task