from app.api.dependencies import SessionDep
from app.models.users import User
from app.schemas.users import CreateUser
from passlib.context import CryptContext
from sqlalchemy import select
from app.core.exceptions import InvalidCredentialsException
from app.config import security_settings
import jwt
from datetime import datetime, timedelta

password_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    pbkdf2_sha256__rounds=300000,
    deprecated="auto"
)

class UserService:
    
    def __init__(self, session: SessionDep):
        self.session = session
    
    async def add(self, create_user: CreateUser) -> User:
        user = User(
            **create_user.model_dump(exclude="password"),
            password = password_context.hash(create_user.password)
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        return user
    
    
    async def create_token(self, user_name, password) -> User:
        query_result = await self.session.execute(
            select(User).where(User.user_name == user_name)
        )
        
        user = query_result.scalar()
                
        if user is None or not password_context.verify(password, user.password):
            raise InvalidCredentialsException()
        
        token = jwt.encode(
            payload={
                "user": {
                    "name": user.user_name,
                },
                "exp": datetime.now() + timedelta(days=1)
            },
            algorithm=security_settings.JWT_ALGORITHM,
            key=security_settings.JWT_SECRET_KEY
        )
        
        return token