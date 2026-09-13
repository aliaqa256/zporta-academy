"""
Domain exceptions for Lessons.
Zero framework dependencies.
"""
from core.shared_kernel.domain.exceptions import DomainException


class LessonNotFoundError(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"Lesson '{identifier}' was not found.",
            code="LESSON_NOT_FOUND",
            details={"identifier": identifier}
        )


class LessonAccessDeniedError(DomainException):
    def __init__(self, message: str = "You do not have permission to view or modify this lesson."):
        super().__init__(message=message, code="LESSON_ACCESS_DENIED")


class InvalidLessonStateError(DomainException):
    def __init__(self, message: str):
        super().__init__(message=message, code="INVALID_LESSON_STATE")
