from typing import Any
from pydantic import BaseModel


class PayloadResponse(BaseModel):
    payload: Any
    httpStatus: int = 200
    message: str = ""
