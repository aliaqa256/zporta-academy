"""
Outbound Port interface for User and Profile persistence.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from users.domain.entities import UserEntity, ProfileEntity, UserPreferenceEntity


class UserRepositoryPort(ABC):
    """Abstract port for User and Profile data access."""

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        ...

    @abstractmethod
    def find_by_credential(self, credential: str) -> Optional[UserEntity]:
        """Finds user by matching username OR email (case-insensitive)."""
        ...

    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        ...

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        ...

    @abstractmethod
    def create_user_with_profile(
        self, username: str, email: str, password_hash: str, role: str, bio: str
    ) -> Tuple[UserEntity, ProfileEntity]:
        ...

    @abstractmethod
    def get_profile_by_user_id(self, user_id: int) -> Optional[ProfileEntity]:
        ...

    @abstractmethod
    def save_profile(self, profile: ProfileEntity) -> ProfileEntity:
        ...

    @abstractmethod
    def get_preferences(self, user_id: int) -> Optional[UserPreferenceEntity]:
        ...
