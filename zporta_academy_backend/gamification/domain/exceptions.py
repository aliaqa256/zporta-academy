class GamificationDomainError(Exception):
    """Base exception for gamification domain."""
    pass


class InvalidActivityTypeError(GamificationDomainError):
    """Raised when an unrecognized activity type is encountered."""
    pass
