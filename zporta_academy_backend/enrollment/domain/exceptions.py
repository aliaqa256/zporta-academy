"""
Enrollment Domain Exceptions.
"""
from core.shared_kernel.domain.exceptions import DomainException, EntityNotFoundError


class EnrollmentError(DomainException):
    """Base exception for enrollment errors."""
    pass


class EnrollmentNotFoundError(EntityNotFoundError):
    """Raised when an enrollment entity is not found."""
    def __init__(self, enrollment_id: int):
        super().__init__(f"Enrollment with ID {enrollment_id} was not found.")
        self.enrollment_id = enrollment_id


class AlreadyEnrolledError(EnrollmentError):
    """Raised when attempting to enroll a user who is already actively enrolled."""
    pass


class InvalidInviteTokenError(EnrollmentError):
    """Raised when a share invite token is invalid or expired."""
    pass
