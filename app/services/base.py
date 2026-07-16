

from sqlmodel import SQLModel
from app.api.dependencies import SessionDep


class BaseService:
    
    def __init__(self, model:SQLModel, session: SessionDep):
        self.session = session
        self.model = model
        
    async def _get(self, id: int):
        return await self.session.get(self.model, id)

    async def _add(self, entity: SQLModel):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
    
    async def _update(self, entity: SQLModel):
        return await self._add(entity) 
    
    async def _delete(self, entity: SQLModel):
        entity.is_deleted = True
        await self.session.commit()
        await self.session.refresh(entity)
        return entity