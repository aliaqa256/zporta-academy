"""
Common pagination DTOs for application layer use cases.
"""
from typing import Generic, TypeVar, List, Optional
from dataclasses import dataclass

T = TypeVar("T")


@dataclass(frozen=True)
class PaginationQueryDTO:
    """Input DTO for paginated queries."""
    page: int = 1
    page_size: int = 20

    def __post_init__(self) -> None:
        if self.page < 1:
            object.__setattr__(self, "page", 1)
        if self.page_size < 1 or self.page_size > 100:
            object.__setattr__(self, "page_size", 20)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


@dataclass(frozen=True)
class PaginatedResultDTO(Generic[T]):
    """Output DTO containing paginated data and metadata."""
    items: List[T]
    total_count: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return (self.total_count + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1
