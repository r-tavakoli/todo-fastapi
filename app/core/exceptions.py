from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Any

class NotFoundException(HTTPException):
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id '{identifier}' not found"
        )
        
    def to_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content={
                "success": False,
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": self.detail,
                    "resource": self.resource,
                    "identifier": str(self.identifier)
                }
            }
        )

class BadRequestException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no data provided"
        )
        
    def to_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content={
                "success": False,
                "error": {
                    "code": "RESOURCE_NOT_FOUND",
                    "message": self.detail,
                }
            }
        )
