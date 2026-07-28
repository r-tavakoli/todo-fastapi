from typing import Annotated

from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenException
from app.core.security import oauth2_scheme
from app.db.redis import jti_is_blacklisted
from app.db.session import get_session
from app.models.users import User
from app.services.notification import NotificationService
from app.services.tasks import TaskService
from app.services.users import UserService
from app.utils import decode_access_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# access token dependency
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = decode_access_token(token)

    if data is None or await jti_is_blacklisted(data["user"]["jti"]):
        raise InvalidTokenException()
    
    return data

# user
async def get_user(token_data: Annotated[dict, Depends(get_access_token)], session: SessionDep):
    user = await session.get(User, token_data["user"]["id"])
    return user

# notification
def get_notification_service(background_tasks: BackgroundTasks) -> NotificationService:
    return NotificationService(background_tasks)

# task
def get_task_service(
    session: SessionDep,
    notification_service: NotificationService = Depends(get_notification_service)
) -> TaskService:
    return TaskService(session, notification_service)

# user
def get_user_service(
    session: SessionDep,
    notification_service: NotificationService = Depends(get_notification_service)
) -> UserService:
    return UserService(session, notification_service)

# dependencies
UserDep = Annotated[User, Depends(get_user)]
TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

