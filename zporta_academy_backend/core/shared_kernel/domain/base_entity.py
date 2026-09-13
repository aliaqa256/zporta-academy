"""
Base Domain Entity abstractions for Hexagonal Architecture.
Pure Python, zero framework dependencies.
"""
from typing import Generic, TypeVar, Any, Optional
from dataclasses import dataclass
from datetime import datetime

ID = TypeVar("ID")


@dataclass(eq=False)
class BaseEntity(Generic[ID]):
    """
    Base domain entity.
    Entities have a distinct identity (id) and are compared by identity rather than attributes.
    """
    id: ID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        if self.id is None:
            raise TypeError("Cannot hash an entity with None id")
        return hash((self.__class__, self.id))
