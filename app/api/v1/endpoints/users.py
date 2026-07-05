from typing import Annotated
from fastapi import APIRouter, Depends
from app.api.dependencies import UserDep, get_access_token
from app.core.exceptions import InvalidCredentialsException
from app.models.users import User
from app.services.users import UserService
from app.schemas.users import CreateUser, CreateUserResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import oauth2_scheme


router = APIRouter()

ServiceDep = Annotated[UserService, Depends()]

@router.post("/register")
async def register_user(create_task: CreateUser, service: ServiceDep) -> CreateUserResponse:
    return await service.add(create_task)

@router.post("/login")
async def login_in(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: ServiceDep) -> dict[str, str]:
    token = await service.create_token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }
    
@router.get("/logout")
async def login_out(token_data: Annotated[dict, Depends(get_access_token)]) -> dict[str, str]:
    return token_data["jit"]

# @router.post("/test") 
# async def test(token: Annotated[str, Depends(oauth2_scheme)], service: ServiceDep) -> User:
#     data = service.decode_token(token)
    
#     if data is None:
#         raise InvalidCredentialsException(message="Invalid access token")
    
#     user = await service.get(data["user"]["id"])
    
#     return user
    
    
# @router.post("/test2") 
# async def test2(user: UserDep, service: ServiceDep) -> User:
#     return user
    