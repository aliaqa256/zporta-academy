"""
Enrollment Repository Port Interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from enrollment.domain.entities import EnrollmentEntity, ShareInviteEntity


class EnrollmentRepositoryPort(ABC):
    """Outbound port for persisting and querying student enrollments and invitations."""

    @abstractmethod
    def get_by_id(self, enrollment_id: int) -> Optional[EnrollmentEntity]:
        """Fetch enrollment by primary key."""
        pass

    @abstractmethod
    def find_enrollment(self, user_id: int, object_id: int, enrollment_type: str = "course") -> Optional[EnrollmentEntity]:
        """Find enrollment for a user and content item."""
        pass

    @abstractmethod
    def list_user_enrollments(self, user_id: int) -> List[EnrollmentEntity]:
        """List all enrollments for a user."""
        pass

    @abstractmethod
    def list_course_enrollments(self, course_id: int) -> List[EnrollmentEntity]:
        """List all student enrollments for a course."""
        pass

    @abstractmethod
    def save(self, enrollment: EnrollmentEntity) -> EnrollmentEntity:
        """Persist or update an enrollment entity."""
        pass

    @abstractmethod
    def find_invite_by_token(self, token: str) -> Optional[ShareInviteEntity]:
        """Find a share invite by token."""
        pass
