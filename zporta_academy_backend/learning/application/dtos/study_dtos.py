"""
Learning Application DTOs.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class LearningRecordDTO:
    id: int
    user_id: int
    enrollment_id: int
    subject_id: Optional[int]
    subject_name: Optional[str]
    content_title: str
    started_at: Optional[datetime] = None


@dataclass(frozen=True)
class StudyDashboardDTO:
    enrolled: List[Dict[str, Any]]
    suggested_courses: List[Dict[str, Any]]
    suggested_quizzes: List[Dict[str, Any]]
    next_lessons: List[Dict[str, Any]]
    suggested_lessons: List[Dict[str, Any]]


@dataclass(frozen=True)
class ReviewCardCommand:
    user_id: int
    item_id: int
    rating: str  # "again", "hard", "good", "easy"


@dataclass(frozen=True)
class ReviewResultDTO:
    item_id: int
    user_id: int
    repetitions: int
    ease_factor: float
    interval_days: int
    next_review_at: datetime
