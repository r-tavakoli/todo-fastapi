from fastapi import FastAPI
from .schemas import ReadTask
from typing import Any
from scalar_fastapi import get_scalar_api_reference
from app.session import SessionDep, create_tables
from app.models import Task
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(
    # Server start/stop listener
    lifespan=lifespan_handler,
)

@app.get("/")
async def read_task(task_id: int, session: SessionDep):
    task = session.get(Task, id)
    return task


# @app.get()
# def create_task():
#     pass

# @app.get()
# def update_task():
#     pass

# @app.get()
# def delete_task():
#     pass


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )