"""
Outbound Port interface for Content Difficulty persistence.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from intelligence.domain.entities import ContentDifficultyEntity


class DifficultyRepositoryPort(ABC):
    """Abstract port for ContentDifficultyProfile persistence."""

    @abstractmethod
    def get_by_content(self, content_type: str, object_id: int) -> Optional[ContentDifficultyEntity]:
        ...

    @abstractmethod
    def save(self, profile: ContentDifficultyEntity) -> ContentDifficultyEntity:
        ...

    @abstractmethod
    def list_difficulties_for_ids(self, content_type: str, object_ids: List[int]) -> List[ContentDifficultyEntity]:
        ...
