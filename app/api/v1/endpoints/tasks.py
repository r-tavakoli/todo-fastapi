from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from app.services.tasks import TaskService
from app.schemas.tasks import ReadTask, CreateTask, CreateeTaskResponse


router = APIRouter(tags=["task"])

ServiceDep = Annotated[TaskService, Depends()]

@router.get("/")
async def get_task(task_id: int, service: ServiceDep) -> ReadTask:
    task = await service.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"id ({task_id}) does not exist"
        )
    return task

@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_task(task: CreateTask, service: ServiceDep) -> CreateeTaskResponse:
    return await service.add(task)


# @app.get()
# def create_task():
#     pass

# @app.get()
# def update_task():
#     pass

# @app.get()
# def delete_task():
#     pass