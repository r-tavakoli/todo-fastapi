from app.api.dependencies import SessionDep
from app.models.users import User
from app.schemas.users import CreateUser
from passlib.context import CryptContext
from sqlalchemy import select
from app.core.exceptions import InvalidCredentialsException
import jwt
from datetime import timedelta
from app.utils import encode_access_token, decode_access_token

password_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    pbkdf2_sha256__rounds=300000,
    deprecated="auto"
)

class UserService:
    
    def __init__(self, session: SessionDep):
        self.session = session
        
    async def get(self, id: int) -> User:
        user = await self.session.get(User, id)
        
        return user        
    
    async def add(self, create_user: CreateUser) -> User:
        user = User(
            **create_user.model_dump(exclude="password"),
            password = password_context.hash(create_user.password)
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        return user
    
    
    async def create_token(self, user_name, password) -> str:
        query_result = await self.session.execute(
            select(User).where(User.user_name == user_name)
        )
        
        user = query_result.scalar()
                
        if user is None or not password_context.verify(password, user.password):
            raise InvalidCredentialsException()
        
        token = encode_access_token(user.id, user.user_name, timedelta(days=1))
        
        return token
    
    def decode_token(self, token: str) -> dict | None:
        try:
            return decode_access_token(token)
        except jwt.PyJWTError:
            return None