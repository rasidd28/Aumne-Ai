from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Title of the article")
    content: str = Field(..., description="Article content between 50 and 2000 characters")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Scaling Distributed Workflows with Python",
                "content": "Building reliable asynchronous systems requires thoughtful idempotency, queue isolation, and robust backoff strategies.",
            }
        }
    )


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    status: str
    flagged_reasons: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostSubmitResponse(BaseModel):
    id: int
    status: str
    flagged_reasons: Optional[str] = None
    message: str


class PostPublishResponse(BaseModel):
    id: int
    status: str
    message: str


class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total: int
