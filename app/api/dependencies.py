from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import InvalidCredentialsException
from app.db.session import get_session
from fastapi import Depends
from app.core.security import oauth2_scheme
from app.models.users import User
from app.utils import decode_access_token
from app.db.redis import jti_is_blacklisted

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# access token dependency
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = decode_access_token(token)

    if data is None or await jti_is_blacklisted(data["user"]["jti"]):
        raise InvalidCredentialsException(message="Invalid or expired access token")
    
    return data

# get user
async def get_user(token_data: Annotated[dict, Depends(get_access_token)], session: SessionDep):
    user = await session.get(User, token_data["user"]["id"])
    return user

UserDep = Annotated[User, Depends(get_user)]