class NotificationDomainError(Exception):
    """Base exception for notification domain."""
    pass


class DeviceTokenNotFoundError(NotificationDomainError):
    """Raised when no active device tokens are found for push dispatch."""
    pass
