from uuid import UUID

from pydantic import BaseModel, constr
from typing import Optional


# Shared base
class PostBase(BaseModel):
    text: constr(min_length=1, max_length=1_000_000)  # Enforce size < 1MB


# For creating a post
class PostCreateSchema(PostBase):
    pass


# For reading posts (e.g., return to client)
class PostResponseSchema(PostBase):
    id: UUID
    user_id: UUID

    class Config:
        orm_mode = True