"""
Generic Base Repository Port interface.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any

EntityT = TypeVar("EntityT")
ID = TypeVar("ID")


class BaseRepositoryPort(ABC, Generic[EntityT, ID]):
    """Generic interface for domain entity persistence."""

    @abstractmethod
    def get_by_id(self, entity_id: ID) -> Optional[EntityT]:
        """Fetch an entity by its identifier."""
        ...

    @abstractmethod
    def save(self, entity: EntityT) -> EntityT:
        """Persist new or updated entity and return the current state."""
        ...

    @abstractmethod
    def delete(self, entity_id: ID) -> bool:
        """Remove entity by its identifier. Returns True if deleted."""
        ...

    @abstractmethod
    def list_all(self, limit: int = 100, offset: int = 0) -> List[EntityT]:
        """Fetch a paginated list of entities."""
        ...
