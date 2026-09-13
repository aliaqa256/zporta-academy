"""
Domain exceptions for Intelligence domain.
"""
from core.shared_kernel.domain.exceptions import DomainException


class AbilityProfileNotFoundError(DomainException):
    def __init__(self, user_id: int):
        super().__init__(f"User ability profile for user ID {user_id} was not found.")


class DifficultyProfileNotFoundError(DomainException):
    def __init__(self, content_type: str, object_id: int):
        super().__init__(f"Difficulty profile for {content_type} #{object_id} was not found.")
