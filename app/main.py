from fastapi import FastAPI
from .schemas import ReadTask
from typing import Any
from scalar_fastapi import get_scalar_api_reference


app = FastAPI()

@app.get("/")
def read_task(task_id: int) -> Any:
    return {
        f"we did it, this is task {task_id}"
    }


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