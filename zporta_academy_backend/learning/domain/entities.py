"""
Learning & Spaced Repetition Domain Entities.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from core.shared_kernel.domain.base_entity import BaseEntity
from learning.domain.value_objects import NotePrivacy, ReviewRating


@dataclass(eq=False)
class StudyItemEntity(BaseEntity[Optional[int]]):
    """Represents a spaced repetition flashcard or learning concept."""
    id: Optional[int] = None
    user_id: int = 0
    title: str = ""
    content_type: str = "lesson"
    object_id: int = 0
    ease_factor: float = 2.5
    interval_days: int = 1
    repetitions: int = 0
    next_review_at: Optional[datetime] = None
    last_reviewed_at: Optional[datetime] = None


@dataclass(eq=False)
class LearningRecordEntity(BaseEntity[Optional[int]]):
    """Represents an active learning enrollment record."""
    id: Optional[int] = None
    enrollment_id: int = 0
    subject_id: Optional[int] = None
    user_id: int = 0
    username: str = ""
    content_title: str = ""
    started_at: Optional[datetime] = None


@dataclass(eq=False)
class UserNoteEntity(BaseEntity[Optional[int]]):
    """Represents a student learning note."""
    id: Optional[int] = None
    user_id: int = 0
    username: str = ""
    text: str = ""
    image_url: Optional[str] = None
    privacy: NotePrivacy = NotePrivacy.PRIVATE
    mentions: List[int] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass(frozen=True)
class StudyDashboardEntity:
    """Aggregated learning dashboard entity."""
    enrolled: List[Dict[str, Any]]
    suggested_courses: List[Dict[str, Any]]
    suggested_quizzes: List[Dict[str, Any]]
    next_lessons: List[Dict[str, Any]]
    suggested_lessons: List[Dict[str, Any]]
