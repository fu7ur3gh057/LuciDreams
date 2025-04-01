from typing import Any

from pydantic import BaseModel


class PaginationResponseSchema(BaseModel):
    data: list[Any]
    total_items: int
    page: int
    size: int
    total_pages: int
