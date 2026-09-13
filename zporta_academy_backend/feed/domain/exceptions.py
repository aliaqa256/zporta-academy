class FeedDomainError(Exception):
    """Base exception for feed domain."""
    pass


class QuizNotFoundError(FeedDomainError):
    """Raised when a requested quiz is not found."""
    pass
