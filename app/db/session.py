from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import db_settings

postgre_engine = create_async_engine(
    url=db_settings.POSTGRES_URL,
    echo=True
)

def get_test_engine():
    test_engine = create_async_engine(
        url=db_settings.TEST_POSTGRES_URL,
        echo=False,
        pool_pre_ping=True,
    )
    return test_engine

async def create_tables(engine: AsyncEngine = postgre_engine):
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
        
async def drop_tables(engine: AsyncEngine = None):
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)        
        
async def get_session():
    async_session = sessionmaker(
        bind=postgre_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        
async def get_test_session():
    test_engine = get_test_engine()
    async_session = sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
        