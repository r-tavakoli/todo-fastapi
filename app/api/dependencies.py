from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from fastapi import Depends


SessionDep = Annotated[AsyncSession, Depends(get_session)]
