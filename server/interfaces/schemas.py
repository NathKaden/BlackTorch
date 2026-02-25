from __future__ import annotations
from pydantic import BaseModel, Field
class GenerateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    negative_text: str = Field(default="")
class GenerateResponse(BaseModel):
    job_id: str
class JobStatusResponse(BaseModel):
    id: str
    status: str
    progress: int
    error_message: str | None = None