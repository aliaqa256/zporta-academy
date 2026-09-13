"""
Outbound Port interface for Subject persistence.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from courses.domain.entities import SubjectEntity
from courses.application.dtos import SubjectDTO


class SubjectRepositoryPort(ABC):
    """Abstract port for Subject database access."""

    @abstractmethod
    def get_by_id(self, subject_id: int) -> Optional[SubjectEntity]:
        ...

    @abstractmethod
    def list_all(self) -> List[SubjectDTO]:
        ...
