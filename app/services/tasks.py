from app.api.dependencies import SessionDep
from app.models.tasks import Task
from app.models.users import User
from app.schemas.tasks import CreateTask, UpdateTask
from app.core.exceptions import NotFoundException
from app.services.base import BaseService

class TaskService(BaseService):
    
    def __init__(self, session: SessionDep):
        super().__init__(Task, session)
    
    async def get(self, id: int) -> Task:
        task = await self._get(id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        return task
    
    async def add(self, create_task: CreateTask, user: User) -> Task:
        task = Task(**create_task.model_dump(), user_id=user.id)      
        return await self._add(task)
    
    async def update(self, id: int , update_task: UpdateTask) -> Task:
        task = await self._get(id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        
        task.sqlmodel_update(update_task)
        
        return await self._update(task)  
    
    async def delete(self, id: int) -> Task:
        task = await self.session.get(Task, id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        
        return await self._delete(task)