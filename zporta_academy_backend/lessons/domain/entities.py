"""
Domain entities for Lessons and Content Gating.
Pure Python, zero framework dependencies.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from core.shared_kernel.domain.base_entity import BaseEntity


@dataclass(eq=False)
class LessonEntity(BaseEntity[int]):
    """Pure domain entity representing a Lesson."""
    title: str = ""
    content: str = ""
    permalink: str = ""
    video_url: str = ""
    subject_id: Optional[int] = None
    course_id: Optional[int] = None
    created_by_id: int = 0
    status: str = "draft"
    is_premium: bool = False
    is_locked: bool = False
    position: int = 0
    published_at: Optional[datetime] = None

    @property
    def is_published(self) -> bool:
        return self.status == "published"


@dataclass(eq=False)
class LessonCompletionEntity(BaseEntity[int]):
    """Pure domain entity representing a Lesson completion event."""
    user_id: int = 0
    lesson_id: int = 0
    completed_at: Optional[datetime] = None
