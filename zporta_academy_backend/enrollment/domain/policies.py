"""
Enrollment Domain Policies.
"""
from typing import List, Optional
from enrollment.domain.entities import EnrollmentEntity
from enrollment.domain.value_objects import EnrollmentStatus, EnrollmentType


class EnrollmentAccessPolicy:
    """Domain policy verifying access grants, premium gating, and enrollment eligibility."""

    @staticmethod
    def has_course_access(
        user_id: int,
        course_id: int,
        enrollments: List[EnrollmentEntity],
        is_course_author: bool = False,
        is_staff: bool = False,
        is_free: bool = False,
    ) -> bool:
        if is_staff or is_course_author or is_free:
            return True

        for e in enrollments:
            if (
                e.user_id == user_id
                and e.object_id == course_id
                and e.enrollment_type == EnrollmentType.COURSE
                and e.is_active()
            ):
                return True

        return False

    @staticmethod
    def can_enroll(
        user_id: int,
        course_id: int,
        existing_enrollment: Optional[EnrollmentEntity],
    ) -> bool:
        if existing_enrollment and existing_enrollment.is_active():
            return False
        return True
