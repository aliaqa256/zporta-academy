"""
Outbound Port interface for Authentication, Password verification, and Token generation.
"""
from abc import ABC, abstractmethod
from typing import Optional, Tuple


class AuthServicePort(ABC):
    """Abstract port for authentication services and token management."""

    @abstractmethod
    def hash_password(self, raw_password: str) -> str:
        ...

    @abstractmethod
    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        ...

    @abstractmethod
    def authenticate_credential(self, username_or_email: str, raw_password: str) -> Optional[int]:
        """Returns user_id if valid credentials, otherwise None."""
        ...

    @abstractmethod
    def get_or_create_token(self, user_id: int) -> str:
        ...
