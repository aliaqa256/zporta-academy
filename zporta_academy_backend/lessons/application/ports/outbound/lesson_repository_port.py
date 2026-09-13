"""
Outbound Port interface for Lesson persistence.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from lessons.domain.entities import LessonEntity
from lessons.application.dtos import LessonFilterQueryDTO, LessonSummaryDTO, LessonDetailDTO


class LessonRepositoryPort(ABC):
    """Abstract port for Lesson database access."""

    @abstractmethod
    def get_by_id(self, lesson_id: int) -> Optional[LessonEntity]:
        ...

    @abstractmethod
    def get_by_permalink(self, permalink: str) -> Optional[LessonEntity]:
        ...

    @abstractmethod
    def list_lessons(self, query: LessonFilterQueryDTO) -> List[LessonSummaryDTO]:
        ...

    @abstractmethod
    def set_status(self, lesson_id: int, status: str) -> LessonEntity:
        ...

    @abstractmethod
    def is_user_enrolled_in_course(self, user_id: int, course_id: int) -> bool:
        ...

    @abstractmethod
    def is_lesson_completed_by_user(self, user_id: int, lesson_id: int) -> bool:
        ...
