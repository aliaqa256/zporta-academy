"""
Domain policies and invariant rules for Courses.
Pure Python, zero framework dependencies.
"""
from typing import Optional, List


class CourseAccessPolicy:
    """Evaluates whether a user can access a course (including draft status)."""
    @staticmethod
    def can_view_course(
        is_draft: bool,
        user_id: Optional[int],
        creator_id: int,
        allowed_tester_ids: List[int],
        is_staff: bool = False,
        is_superuser: bool = False
    ) -> bool:
        if not is_draft:
            return True
        if user_id is None:
            return False
        return (
            user_id == creator_id
            or user_id in allowed_tester_ids
            or is_staff
            or is_superuser
        )

    @staticmethod
    def can_edit_course(user_id: Optional[int], creator_id: int, is_locked: bool, is_staff: bool = False) -> bool:
        if user_id is None:
            return False
        if is_locked and not is_staff:
            return False
        return user_id == creator_id or is_staff
