"""
Domain entities for Courses and Subjects.
Pure Python, zero framework dependencies.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from core.shared_kernel.domain.base_entity import BaseEntity


@dataclass(eq=False)
class SubjectEntity(BaseEntity[int]):
    """Pure domain entity representing a Subject."""
    name: str = ""
    permalink: str = ""
    created_by_id: int = 0


@dataclass(eq=False)
class CourseEntity(BaseEntity[int]):
    """Pure domain entity representing a Course."""
    title: str = ""
    description: str = ""
    permalink: str = ""
    cover_image_url: Optional[str] = None
    subject_id: Optional[int] = None
    created_by_id: int = 0
    price: float = 0.00
    course_type: str = "free"
    is_draft: bool = True
    is_locked: bool = False
    allowed_tester_ids: List[int] = field(default_factory=list)

    @property
    def is_published(self) -> bool:
        return not self.is_draft

    @property
    def is_premium(self) -> bool:
        return self.course_type == "premium" or self.price > 0
