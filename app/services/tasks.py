from app.api.dependencies import SessionDep
from app.models.tasks import Task
from app.schemas.tasks import CreateTask, UpdateTask
from app.core.exceptions import NotFoundException

class TaskService:
    
    def __init__(self, session: SessionDep):
        self.session = session
    
    async def get(self, id: int) -> Task:
        task = await self.session.get(Task, id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        return task
    
    async def add(self, create_task: CreateTask) -> Task:
        task = Task(**create_task.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        
        return task
    
    async def update(self, id: int , update_task: UpdateTask) -> Task:
        task = await self.session.get(Task, id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        
        task.sqlmodel_update(update_task)
        
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        
        return task    
    
    async def delete(self, id: int) -> Task:
        task = await self.session.get(Task, id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        task.is_deleted = True
        await self.session.commit()
        await self.session.refresh(task)
        
        return task        