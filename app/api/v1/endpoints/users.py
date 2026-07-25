from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from app.api.dependencies import UserServiceDep, get_access_token
from app.schemas.users import CreateUser, CreateUserResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.db.redis import add_jti_to_blacklist
from app.utils import TEMPLATE_PATH
from app.config import app_settings

router = APIRouter()


templates = Jinja2Templates(directory=TEMPLATE_PATH/"pages")

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
    
@router.get("/forgot_password")
async def forgot_password(email: EmailStr, service: UserServiceDep) -> dict[str, str]:
    await service.send_reset_password_link(email)
    return {
        "detail": "Check email for password reset link"
    }    
    
@router.get("/reset_password_form")
async def get_reset_password_form(request: Request, token: str):
    print('='*60)
    print(f"{app_settings.APP_DOMAIN}/api/{app_settings.APP_API_VERSION}/users/reset_password?token={token}")
    return templates.TemplateResponse(
        request,
        name="reset_password.html",
        context={
            "reset_url": f"{app_settings.APP_DOMAIN}/api/{app_settings.APP_API_VERSION}/users/reset_password?token={token}",
        }
    )
    
@router.post("/reset_password")
async def reset_password(token: str, password: Annotated[str, Form()], service: UserServiceDep) -> dict[str, str]:
    await service.reset_password(token, password, expiry=timedelta(hours=24))    
    return {
        "detail": "Password changed!"
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
    