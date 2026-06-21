from app.api.dependencies import SessionDep
from app.models.users import User
from app.schemas.users import CreateUser
from app.core.exceptions import NotFoundException
from passlib.context import CryptContext

password_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    pbkdf2_sha256__rounds=300000,
    deprecated="auto"
)

class UserService:
    
    def __init__(self, session: SessionDep):
        self.session = session
    
    async def add(self, create_user: CreateUser) -> User:
        print(create_user.password, "="*100)
        user = User(
            **create_user.model_dump(exclude="password"),
            password = password_context.hash(create_user.password)
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        return user