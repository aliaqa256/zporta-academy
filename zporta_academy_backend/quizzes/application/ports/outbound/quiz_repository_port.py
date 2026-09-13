"""
Outbound Port interface for Quiz persistence.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from quizzes.domain.entities import QuizEntity
from quizzes.application.dtos import QuizSummaryDTO, QuizDetailDTO


class QuizRepositoryPort(ABC):
    """Abstract port for Quiz database access."""

    @abstractmethod
    def get_by_id(self, quiz_id: int) -> Optional[QuizEntity]:
        ...

    @abstractmethod
    def get_by_permalink(self, permalink: str) -> Optional[QuizEntity]:
        ...

    @abstractmethod
    def list_published(self, created_by_username: Optional[str] = None) -> List[QuizSummaryDTO]:
        ...

    @abstractmethod
    def set_status(self, quiz_id: int, status: str) -> QuizEntity:
        ...
