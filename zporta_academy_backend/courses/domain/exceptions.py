"""
Domain exceptions for Courses and Subjects.
Zero framework dependencies.
"""
from core.shared_kernel.domain.exceptions import DomainException


class CourseNotFoundError(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"Course '{identifier}' was not found.",
            code="COURSE_NOT_FOUND",
            details={"identifier": identifier}
        )


class SubjectNotFoundError(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"Subject '{identifier}' was not found.",
            code="SUBJECT_NOT_FOUND",
            details={"identifier": identifier}
        )


class CourseAccessDeniedError(DomainException):
    def __init__(self, message: str = "You do not have permission to view this course."):
        super().__init__(message=message, code="COURSE_ACCESS_DENIED")


class CannotDraftEnrolledCourseError(DomainException):
    def __init__(self, message: str = "Cannot set course to draft because active enrollments exist."):
        super().__init__(message=message, code="CANNOT_DRAFT_ENROLLED_COURSE")
