from datetime import datetime

from app.models.tasks import Task, TaskHistory
from app.models.users import User
from app.schemas.tasks import CreateTask, UpdateTask
from app.core.exceptions import NotFoundException
from app.services.base import BaseService, HistoryTracker
from app.services.notification import NotificationService
from sqlalchemy.ext.asyncio import AsyncSession

class TaskService(BaseService):
    def __init__(self, session: AsyncSession, notification_service: NotificationService):
        super().__init__(Task, session)
        self.history_tracker = HistoryTracker(
            model=Task,
            history_model=TaskHistory,
            entity_id_field_name="task_id"
        )
        self.notification_service = notification_service
    
    async def get(self, id: int) -> Task:
        task = await self._get(id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        return task
    
    async def add(self, create_task: CreateTask, user: User) -> Task:
        task = Task(**create_task.model_dump(), user_id=user.id)     
        task = await self._add(task)
        return task
    
    async def update(self, id: int , update_task: UpdateTask, user: User) -> Task:
        task = await self._get(id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        
        before = self.history_tracker.track_history(task)
        task.sqlmodel_update(update_task)
        task = await self._update(task) 
        history = self.history_tracker.create_history(before, task)

        if history:
            await self.add_task_history(history, user.id)
        await self._notifiy(task, user)

        return task
    
    async def delete(self, id: int) -> Task:
        task = await self.session.get(Task, id)
        if not task or task.is_deleted:
            raise NotFoundException("Task", id)
        
    async def add_task_history(self, task_history: TaskHistory, user_id: int):
        task_history = TaskHistory(**task_history.model_dump(), user_id=user_id)      
        return await self._add(task_history)        
        
    async def _notifiy(self, task: Task, user: User):
        if task.status_id == 3:
            await self.notification_service.send_email(
                recipients=[user.email],
                subject="Task is DONE",
                context={
                    "task_title": task.title,
                    "task_status_id": task.status_id,
                    "now": datetime.now()
                },
                template_name="email_task.html"
            )