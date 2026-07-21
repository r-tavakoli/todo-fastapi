from app.core.exceptions import BadRequestException
from fastapi import APIRouter
from fastapi import status
from app.schemas.tasks import ReadTaskResponse, CreateTask, CreateTaskResponse, UpdateTask, UpdateTaskResponse, DeleteTaskResponse
from app.api.dependencies import TaskServiceDep, UserDep

router = APIRouter()

@router.get("/")
async def get_task(user: UserDep, task_id: int, service: TaskServiceDep) -> ReadTaskResponse:
    task = await service.get(task_id)
    return task

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_task(user: UserDep, create_task: CreateTask, service: TaskServiceDep) -> CreateTaskResponse:
    return await service.add(create_task, user)

@router.patch("/update")
async def update_task(user: UserDep, id: int, update_task: UpdateTask, service: TaskServiceDep) -> UpdateTaskResponse:
    task = update_task.model_dump(exclude_none=True)
    if not task:
        raise BadRequestException()
    return await service.update(id, task, user)

@router.delete("/delete")
async def delete_task(user: UserDep, id: int, service: TaskServiceDep) -> DeleteTaskResponse:
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