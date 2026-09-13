"""
Application Layer DTOs for Lessons.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass(frozen=True)
class LessonSummaryDTO:
    id: int
    title: str
    permalink: str
    content_preview: str
    subject_id: Optional[int]
    subject_name: Optional[str]
    course_id: Optional[int]
    course_title: Optional[str]
    created_by_id: int
    created_by_name: str
    status: str
    is_premium: bool
    is_locked: bool
    position: int
    created_at: str


@dataclass(frozen=True)
class LessonDetailDTO:
    id: int
    title: str
    content: str
    permalink: str
    video_url: str
    subject_id: Optional[int]
    subject_name: Optional[str]
    course_id: Optional[int]
    course_title: Optional[str]
    created_by_id: int
    created_by_name: str
    status: str
    is_premium: bool
    is_locked: bool
    is_gated: bool
    is_completed: bool
    is_owner: bool
    position: int
    canonical_url: str


@dataclass(frozen=True)
class CompleteLessonCommand:
    lesson_id: int
    user_id: int


@dataclass(frozen=True)
class LessonCompletionResultDTO:
    lesson_id: int
    user_id: int
    points_awarded: int
    message: str


@dataclass(frozen=True)
class LessonFilterQueryDTO:
    course_id: Optional[int] = None
    subject_id: Optional[int] = None
    status: Optional[str] = None
    user_id: Optional[int] = None
