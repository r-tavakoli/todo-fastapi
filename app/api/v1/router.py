from fastapi import APIRouter
from app.api.v1.endpoints import tasks, users


v1_router = APIRouter()

v1_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
v1_router.include_router(users.router, prefix="/users", tags=["users"])
