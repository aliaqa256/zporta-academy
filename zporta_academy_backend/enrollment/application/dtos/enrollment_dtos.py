"""
Enrollment Application DTOs.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class EnrollUserCommand:
    """Command requesting enrollment in a course or content item."""
    user_id: int
    object_id: int
    enrollment_type: str = "course"
    status: str = "active"


@dataclass(frozen=True)
class EnrollmentDTO:
    id: int
    user_id: int
    username: str
    object_id: int
    content_title: str
    enrollment_type: str
    status: str
    enrollment_date: Optional[datetime] = None


@dataclass(frozen=True)
class CheckAccessQuery:
    user_id: int
    course_id: int
    is_staff: bool = False


@dataclass(frozen=True)
class AccessResultDTO:
    has_access: bool
    reason: str
