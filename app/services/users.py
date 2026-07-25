from pydantic import EmailStr

from app.models.users import User
from app.schemas.users import CreateUser
from passlib.context import CryptContext
from sqlalchemy import select
from app.core.exceptions import BadRequestException, InvalidCredentialsException
import jwt
from datetime import timedelta
from app.services.base import BaseService
from app.services.notification import NotificationService
from app.utils import encode_access_token, decode_access_token, generate_url_safe_token, decode_url_safe_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import app_settings


password_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    pbkdf2_sha256__rounds=300000,
    deprecated="auto"
)

class UserService(BaseService):
    
    def __init__(self, session: AsyncSession, notification_service = NotificationService):
        super().__init__(User, session)
        self.notification_service = notification_service
        
    async def get(self, id: int) -> User:
        return self._get(User, id)        
    
    async def add(self, create_user: CreateUser) -> User:
        # Check if user_name already exists
        existing_user = await self.session.execute(
            select(User).where(User.user_name == create_user.user_name)
        )
        existing_user = existing_user.scalar_one_or_none()
        
        if existing_user:
            raise BadRequestException(detail=f"Username '{create_user.user_name}' is already taken")
        
        # Check if email already exists
        existing_email = await self.session.execute(
            select(User).where(User.email == create_user.email)
        )
        existing_email = existing_email.scalar_one_or_none()
        
        if existing_email:
            raise BadRequestException(detail=f"Email '{create_user.email}' is already registered")        
        
        # Create user
        user = User(
            **create_user.model_dump(exclude="password"),
            password = password_context.hash(create_user.password)
        )
        
        user = await self._add(user)
        
        # Create verification url token
        token = generate_url_safe_token(
            {
                "email": user.email,
                "id": user.id
            },
            salt="email_verification"
        )
        
        # Sending verification email
        await self.send_verification_link(
            user,
            verification_url_token=token
        )
        
        return user
    
    
    async def _get_credential_by_user_name(self, user_name):
        query_result = await self.session.execute(
            select(User).where(User.user_name == user_name)
        )
        
        user = query_result.scalar()  
        
        if user is None:
            raise InvalidCredentialsException()
        
        return user
    
    async def _get_credential_by_email(self, email):
        query_result = await self.session.execute(
            select(User).where(User.email == email)
        )
        
        user = query_result.scalar()  
        
        if user is None:
            raise InvalidCredentialsException()
        
        return user    
    
    
    async def create_token(self, user_name, password) -> str:
        user = await self._get_credential_by_user_name(user_name)
                
        if not password_context.verify(password, user.password):
            raise InvalidCredentialsException()
        
        token = encode_access_token(user.id, user.user_name, timedelta(days=1))
        
        return token
    
    def decode_token(self, token: str) -> dict | None:
        try:
            return decode_access_token(token)
        except jwt.PyJWTError:
            return None
        
    async def verify_email(self, token: str, expiry: timedelta | None = None):
        token_data = decode_url_safe_token(
            token,
            expiry=expiry,
            salt="email_verification",
        )     
        
        if not token_data:
            raise BadRequestException(detail="Invalid Token")
        
        user = await self._get(token_data["id"])
        
        if not user:
            raise BadRequestException(detail="User not found") 
        
        if not user.is_email_verified:
            user.is_email_verified = True
            await self._update(user)
        
    async def send_verification_link(self, user: User, verification_url_token: str):
        if not user.is_email_verified:
            await self.notification_service.send_email(
                recipients=[user.email],
                subject="Email Verification",
                context={
                    "first_name": user.first_name,
                    "verification_url": f"{app_settings.APP_DOMAIN}/api/{app_settings.APP_API_VERSION}/users/verify?token={verification_url_token}",
                    "expiry": "24 hours",
                    "app_name": app_settings.APP_NAME
                },
                template_name="email/email_verification.html"
            )
            
    async def send_reset_password_link(self, email: EmailStr):
        user = await self._get_credential_by_email(email)
        
        user_data = {
            "email": user.email,
            "id": user.id
        }
        
        token = generate_url_safe_token(user_data, salt="password_reset")
        
        await self.notification_service.send_email(
            recipients=[user.email],
            subject="Reset Password",
            context={
                "first_name": user.first_name,
                "reset_url": f"{app_settings.APP_DOMAIN}/api/{app_settings.APP_API_VERSION}/users/reset_password_form?token={token}",
                "expiry": "24 hours"
            },
            template_name="email/reset_password.html"
        )
        
    async def reset_password(self, token: str, password: str, expiry: timedelta | None = None):
        token_data = decode_url_safe_token(
            token,
            expiry=expiry,
            salt="password_reset",
        )     
        
        if not token_data:
            raise BadRequestException(detail="Invalid Token")
        
        user = await self._get(token_data["id"])
        
        if not user:
            raise BadRequestException(detail="User not found") 
        
        user.password = password_context.hash(password)
        
        await self._update(user)
        
        