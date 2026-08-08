from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.api.v1.router import v1_router
from app.core.exceptions import add_exception_handlers
from app.core.logging import setup_logging
from app.db.session import create_tables
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.timing import TimingMiddleware

setup_logging()


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(
    title="ToDo App",
    # description="Tasks will be done one day",
    # # docs_url=None,
    # # redoc_url=None,
    # version="0.1.0",
    # # terms_of_service=,
    # contact={
    #     "name": "ToDo Support",
    #     "url": "",
    #     "email": "rahtav68@gmail.com"
    # },
    # Server start/stop listener
    lifespan=lifespan_handler,
)

# middlewares (for logging)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)
app.add_middleware(LoggingMiddleware)

# exception hanlder
add_exception_handlers(app)

app.include_router(v1_router, prefix="/api/v1")



@app.get("/test")
def get_test():
    return {"test": "everything is fine"}

### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
