"""
Domain policies and invariant rules for Users and Authentication.
Pure Python, zero framework dependencies.
"""
import re
from typing import Tuple


class PasswordPolicy:
    """Enforces minimum password complexity rules."""
    MIN_LENGTH = 8

    @classmethod
    def validate(cls, password: str) -> Tuple[bool, str]:
        if not password or len(password) < cls.MIN_LENGTH:
            return False, f"Password must be at least {cls.MIN_LENGTH} characters long."
        return True, ""


class RolePermissionPolicy:
    """Enforces role-based capabilities."""
    @staticmethod
    def can_create_courses(role: str, active_guide: bool) -> bool:
        return role in ("guide", "both") or active_guide

    @staticmethod
    def can_invite_other_teachers(role: str, can_invite: bool) -> bool:
        return (role in ("guide", "both")) and can_invite


class ScoreCalculationPolicy:
    """Pure domain scoring calculation formulas."""
    @staticmethod
    def calculate_growth_score(quiz_count: int, lesson_count: int, course_count: int) -> int:
        """🌱 Growth Score: +1 per quiz, +2 per lesson, +3 per course completed"""
        return (quiz_count * 1) + (lesson_count * 2) + (course_count * 3)

    @staticmethod
    def calculate_impact_score(free_enrollments: int, premium_enrollments: int, first_attempts: int) -> int:
        """Impact Score: +2 per free enrollment, +3 per premium, +1 per first student quiz attempt"""
        return (free_enrollments * 2) + (premium_enrollments * 3) + (first_attempts * 1)
