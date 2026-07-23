from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from app.api.dependencies import UserServiceDep, get_access_token
from app.schemas.users import CreateUser, CreateUserResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.db.redis import add_jti_to_blacklist

router = APIRouter()


@router.post("/register")
async def register_user(create_task: CreateUser, service: UserServiceDep) -> CreateUserResponse:
    return await service.add(create_task)

@router.post("/login")
async def login(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: UserServiceDep) -> dict[str, str]:
    token = await service.create_token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }
    
@router.get("/logout")
async def logout(token_data: Annotated[dict, Depends(get_access_token)]) -> dict[str, str]:
    await add_jti_to_blacklist(token_data["user"]["jti"])
    return {
        "detail": "Successfully logged out"
    }

@router.get("/verify")
async def verify(token: str, service: UserServiceDep) -> dict[str, str]:
    await service.verify_email(token, expiry=timedelta(hours=24))
    return {
        "detail": "Account is verified"
    }

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
    