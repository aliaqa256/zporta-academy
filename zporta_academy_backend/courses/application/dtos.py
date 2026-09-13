"""
Application DTOs for Courses and Subjects.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass(frozen=True)
class CourseSummaryDTO:
    id: int
    title: str
    description: str
    permalink: str
    price: float
    course_type: str
    cover_image_url: Optional[str]
    subject_id: Optional[int]
    subject_name: Optional[str]
    created_by_id: int
    created_by_name: str
    lesson_count: int
    is_draft: bool
    is_locked: bool


@dataclass(frozen=True)
class CourseDetailDTO:
    id: int
    title: str
    description: str
    permalink: str
    price: float
    course_type: str
    cover_image_url: Optional[str]
    subject_id: Optional[int]
    subject_name: Optional[str]
    created_by_id: int
    created_by_name: str
    lesson_count: int
    is_draft: bool
    is_locked: bool
    is_owner: bool = False
    canonical_url: str = ""


@dataclass(frozen=True)
class SubjectDTO:
    id: int
    name: str
    permalink: str
    created_by_id: int


@dataclass(frozen=True)
class CourseFilterQueryDTO:
    subject_id: Optional[int] = None
    search_query: Optional[str] = None
    include_drafts: bool = False
    user_id: Optional[int] = None
