from typing import Annotated
from fastapi import APIRouter, Depends
from app.core.exceptions import InvalidCredentialsException
from app.services.users import UserService
from app.schemas.users import CreateUser, CreateUserResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import oauth2_scheme


router = APIRouter()

ServiceDep = Annotated[UserService, Depends()]

@router.post("/register")
async def register_user(create_task: CreateUser, service: ServiceDep) -> CreateUserResponse:
    return await service.add(create_task)

@router.post("/token")
async def create_token(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: ServiceDep) -> dict[str, str]:
    token = await service.create_token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt"
    }

@router.post("/test") 
def test(token: Annotated[str, Depends(oauth2_scheme)], service: ServiceDep):
    token = service.decode_access_token(token)
    
    if token is None:
        raise InvalidCredentialsException(message="Invalid access token")
    
    return {
        "details": "Successfully authenticated"
    }
    
    