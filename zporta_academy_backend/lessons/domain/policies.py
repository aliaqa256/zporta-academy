"""
Domain policies for Lesson access, content gating, and publishing rules.
Pure Python, zero framework dependencies.
"""
from typing import Optional, Tuple
from .value_objects import ContentAccessLevel


class ContentGatingPolicy:
    """Evaluates whether content is fully accessible or gated/truncated."""
    PREVIEW_LENGTH = 300

    @classmethod
    def evaluate_access(
        cls,
        is_premium: bool,
        user_id: Optional[int],
        creator_id: int,
        is_enrolled: bool,
        is_staff: bool = False,
        is_superuser: bool = False
    ) -> ContentAccessLevel:
        if not is_premium:
            return ContentAccessLevel.FULL
        if user_id is None:
            return ContentAccessLevel.PREVIEW
        if user_id == creator_id or is_staff or is_superuser or is_enrolled:
            return ContentAccessLevel.FULL
        return ContentAccessLevel.PREVIEW

    @classmethod
    def process_content(cls, raw_content: str, access_level: ContentAccessLevel) -> Tuple[str, bool]:
        """Returns (content, is_gated). Truncates if preview mode."""
        if access_level == ContentAccessLevel.FULL:
            return raw_content, False
        if len(raw_content) <= cls.PREVIEW_LENGTH:
            return raw_content, True
        truncated = raw_content[:cls.PREVIEW_LENGTH] + "... [Preview: Enroll in course to unlock full lesson]"
        return truncated, True


class LessonPublishPolicy:
    """Enforces invariants when publishing lessons."""
    @staticmethod
    def validate_publishable(
        is_premium: bool,
        has_course: bool,
        is_course_premium: bool = False,
        is_course_draft: bool = False
    ) -> Tuple[bool, str]:
        if is_premium:
            if not has_course or not is_course_premium:
                return False, "Premium lessons must be attached to a premium course before publishing."
        if has_course and is_course_draft:
            return False, "Cannot publish a lesson while its course is in draft. Publish the course first or save the lesson as draft."
        return True, ""

