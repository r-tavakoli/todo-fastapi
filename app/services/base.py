from datetime import datetime
from typing import TypeVar, Generic, Type, List, Dict, Any
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
    
    

T = TypeVar('T', bound=SQLModel)
H = TypeVar('H', bound=SQLModel)

class HistoryTracker(Generic[T, H]):     
    def __init__(
        self,
        model: Type[T],
        history_model: Type[H],
        exclude_fields: List[str] = None,
        extra_fields: Dict[str, Any] = None,
        entity_id_field_name: str = "entity_id"
    ):
        self.model = model
        self.history_model = history_model
        self.exclude_fields = exclude_fields or ['id', 'created_on', 'modified_on']
        self.extra_fields = extra_fields or {}
        self.entity_id_field_name = entity_id_field_name
    
    def _get_data(self, entity: T) -> Dict[str, Any]:
        state = {}
        from sqlalchemy import inspect
        for column in inspect(entity.__class__).columns:
            field_name = column.name
            if field_name not in self.exclude_fields:
                value = getattr(entity, field_name)
                if isinstance(value, datetime):
                    value = value.isoformat()
                state[field_name] = value
        return state
    
    
    def _extract_data_changes(self, before: Dict, after: Dict):
        before_ = {}
        after_ = {}
        if before != after:
            for key in after.keys():
                if key in before and before[key] != after[key]:
                    before_[key] = before[key]
                    after_[key] = after[key] 
        return before_, after_
        
    def track_history(self, entity: T) -> Dict:
        return self._get_data(entity)
    
    def create_history(self, before: Dict, after: T, operation="update") -> H:
        after_dict = self._get_data(after)
        
        before_change, after_change = self._extract_data_changes(before, after_dict)

        if not after_change:
            return None
        
        history = self.history_model(
            operation=operation,
            before=before_change,
            after=after_change
        )
        
        setattr(history, self.entity_id_field_name, after.id)
        
        return history