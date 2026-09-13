class SocialDomainError(Exception):
    """Base exception for social domain."""
    pass


class GuideRequestAlreadyExistsError(SocialDomainError):
    """Raised when a user attempts to send a duplicate request."""
    pass


class UnauthorizedSocialActionError(SocialDomainError):
    """Raised when an unauthorized user attempts to perform a request action."""
    pass


class GuideRequestNotFoundError(SocialDomainError):
    """Raised when a guide request cannot be found."""
    pass
