from typing import Annotated, Any

from fastapi import Depends, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_session

DatabaseSession = Annotated[Session, Depends(get_session)]
ResourceId = Annotated[int, Path(gt=0, le=2147483647)]


class ErrorResponse(BaseModel):
    detail: str


class InvalidDataResponse(BaseModel):
    detail: str | list[dict[str, Any]]


ERROR_RESPONSES = {
    404: {"model": ErrorResponse, "description": "Project or activity not found"},
    422: {
        "model": InvalidDataResponse,
        "description": "Invalid request or storage constraints",
    },
    503: {"model": ErrorResponse, "description": "Database temporarily unavailable"},
}
