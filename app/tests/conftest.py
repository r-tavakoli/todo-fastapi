from datetime import datetime
from time import perf_counter

import pytest
from httpx import ASGITransport, AsyncClient
from pytest_asyncio.plugin import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.config import db_settings
from app.db.session import create_tables, get_session, get_test_engine
from app.main import app

test_engine = create_async_engine(
    url=db_settings.POSTGRES_TEST_DB_URL,
    echo=False,
    pool_pre_ping=True,
)

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database session for each test with transaction rollback.
    """
    
    test_engine = get_test_engine()
    await create_tables(test_engine)
    
    # Start a transaction
    async with test_engine.connect() as conn:
        trans = await conn.begin()
        
        session = AsyncSession(
            bind=conn,
            expire_on_commit=False,
        )
        
        # override the get_db dependency
        async def override_get_db():
            try:
                yield session
            finally:
                pass  # don't close the session here, we'll rollback the transaction
        
        # apply override
        app.dependency_overrides[get_session] = override_get_db
        
        yield session
        
        # Rollback the transaction after the test
        await trans.rollback()
        await conn.close()
    
    # clear the override after test
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://localhost:8000",
        ) as client:
            yield client
    
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    # setup: record start time
    start_time = perf_counter()
    print(f"\n🧪 Tests started at: {datetime.now().strftime('%H:%M:%S')}")  # noqa: DTZ005
    print("=" * 50)
    
    yield 
    
    # teardown: calculate and display total time
    total_time = perf_counter() - start_time
    print("=" * 50)
    print(f"✅ Tests completed in: {total_time:.2f}s")
    print(f"📅 Finished at: {datetime.now().strftime('%H:%M:%S')}")  # noqa: DTZ005
