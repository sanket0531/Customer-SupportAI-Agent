from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    page: int = Field(
        default=1,
        ge=1,
        description="Page number"
    )

    size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Items per page"
    )

from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def create(
        cls,
        *,
        items: list[T],
        total: int,
        page: int,
        size: int,
    ):
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            total_pages=ceil(total / size) if size else 0,
        )    