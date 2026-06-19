from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.db.session import create_tables
from contextlib import asynccontextmanager
from app.api.v1.router import v1_router


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    # Server start/stop listener
    lifespan=lifespan_handler,
)

app.include_router(v1_router, prefix="/api/v1")


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
