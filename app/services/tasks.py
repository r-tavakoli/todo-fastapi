from app.api.dependencies import SessionDep
from app.models.tasks import Task, TaskHistory
from app.models.users import User
from app.schemas.tasks import CreateTask, UpdateTask
from app.core.exceptions import NotFoundException
from app.services.base import BaseService, HistoryTracker

class TaskService(BaseService):
    
    def __init__(self, session: SessionDep):
        super().__init__(Task, session)
        self.history_tracker = HistoryTracker(
            model=Task,
            history_model=TaskHistory,
            entity_id_field_name="task_id"
        )
    
    async def get(self, id: int) -> Task:
        task = await self._get(id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        return task
    
    async def add(self, create_task: CreateTask, user: User) -> Task:
        task = Task(**create_task.model_dump(), user_id=user.id)      
        return await self._add(task)
    
    async def update(self, id: int , update_task: UpdateTask, user: User) -> Task:
        task = await self._get(id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        
        before = self.history_tracker.track_history(task)
        task.sqlmodel_update(update_task)
        task = await self._update(task) 
        history = self.history_tracker.create_history(before, task)
        
        await self.add_task_history(history, user.id)

        return task
    
    async def delete(self, id: int) -> Task:
        task = await self.session.get(Task, id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        
    async def add_task_history(self, task_history: TaskHistory, user_id: int):
        task_history = TaskHistory(**task_history.model_dump(), user_id=user_id)      
        return await self._add(task_history)        
        