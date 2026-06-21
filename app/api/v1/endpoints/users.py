from typing import Annotated
from fastapi import APIRouter, Depends
from app.services.users import UserService
from app.schemas.users import CreateUser, CreateUserResponse


router = APIRouter()

ServiceDep = Annotated[UserService, Depends()]

@router.post("/register")
async def register_user(create_task: CreateUser, service: ServiceDep) -> CreateUserResponse:
    return await service.add(create_task)