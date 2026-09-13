"""
Enrollment Domain Entities.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from core.shared_kernel.domain.base_entity import BaseEntity
from enrollment.domain.value_objects import EnrollmentStatus, EnrollmentType


@dataclass(eq=False)
class EnrollmentEntity(BaseEntity[Optional[int]]):
    """Represents a student enrollment in a course, quiz, or lesson."""
    id: Optional[int] = None
    user_id: int = 0
    username: str = ""
    content_type_id: int = 0
    content_type_name: str = "course"
    object_id: int = 0
    content_title: str = ""
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE
    enrollment_type: EnrollmentType = EnrollmentType.COURSE
    enrollment_date: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.status == EnrollmentStatus.ACTIVE


@dataclass(eq=False)
class ShareInviteEntity(BaseEntity[Optional[int]]):
    """Represents an invitation token for collaborative learning."""
    id: Optional[int] = None
    enrollment_id: int = 0
    invited_user_id: int = 0
    invited_by_id: int = 0
    token: str = ""
    created_at: Optional[datetime] = None
