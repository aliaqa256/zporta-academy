"""
Learning & Spaced Repetition Domain Exceptions.
"""
from core.shared_kernel.domain.exceptions import DomainException, EntityNotFoundError, UnauthorizedDomainActionError


class LearningDomainError(DomainException):
    """Base exception for learning domain errors."""
    pass


class StudyCardNotFoundError(EntityNotFoundError):
    """Raised when a study card or item cannot be found."""
    def __init__(self, item_id: int):
        super().__init__(f"Study item {item_id} was not found.")
        self.item_id = item_id


class NotePermissionDeniedError(UnauthorizedDomainActionError):
    """Raised when an unauthorized user attempts to edit a note."""
    def __init__(self, message: str = "Permission denied to edit note."):
        super().__init__(message)


class InvalidReviewRatingError(LearningDomainError):
    """Raised when an invalid review rating value is passed."""
    pass
