from typing import Annotated
from app.core.exceptions import BadRequestException
from fastapi import APIRouter, Depends
from fastapi import status
from app.services.tasks import TaskService
from app.schemas.tasks import ReadTaskResponse, CreateTask, CreateTaskResponse, UpdateTask, UpdateTaskResponse, DeleteTaskResponse


router = APIRouter()

ServiceDep = Annotated[TaskService, Depends()]

@router.get("/")
async def get_task(task_id: int, service: ServiceDep) -> ReadTaskResponse:
    task = await service.get(task_id)
    return task

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_task(create_task: CreateTask, service: ServiceDep) -> CreateTaskResponse:
    return await service.add(create_task)

@router.patch("/update")
async def update_task(id: int, update_task: UpdateTask, service: ServiceDep) -> UpdateTaskResponse:
    task = update_task.model_dump(exclude_none=True)
    if not task:
        raise BadRequestException()
    return await service.update(id, task)

@router.delete("/delete")
async def delete_task(id: int, service: ServiceDep) -> DeleteTaskResponse:
    return await service.delete(id)

# @app.get()
# def create_task():
#     pass

# @app.get()
# def update_task():
#     pass

# @app.get()
# def delete_task():
#     pass