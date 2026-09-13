"""
Outbound Port interface for Lesson Completion tracking.
"""
from abc import ABC, abstractmethod
from typing import Optional
from lessons.domain.entities import LessonCompletionEntity


class LessonCompletionRepositoryPort(ABC):
    """Abstract port for recording and querying lesson completions."""

    @abstractmethod
    def record_completion(self, user_id: int, lesson_id: int) -> LessonCompletionEntity:
        ...

    @abstractmethod
    def get_completion(self, user_id: int, lesson_id: int) -> Optional[LessonCompletionEntity]:
        ...
