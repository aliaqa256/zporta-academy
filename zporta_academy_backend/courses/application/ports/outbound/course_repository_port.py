"""
Outbound Port interface for Course persistence.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from courses.domain.entities import CourseEntity
from courses.application.dtos import CourseFilterQueryDTO, CourseSummaryDTO, CourseDetailDTO


class CourseRepositoryPort(ABC):
    """Abstract port for Course database access."""

    @abstractmethod
    def get_by_id(self, course_id: int) -> Optional[CourseEntity]:
        ...

    @abstractmethod
    def get_by_permalink(self, permalink: str) -> Optional[CourseEntity]:
        ...

    @abstractmethod
    def list_courses(self, filter_query: CourseFilterQueryDTO) -> List[CourseSummaryDTO]:
        ...

    @abstractmethod
    def set_draft_status(self, course_id: int, is_draft: bool) -> CourseEntity:
        ...

    @abstractmethod
    def has_active_enrollments(self, course_id: int) -> bool:
        ...
