"""
Outbound Port interface for User Ability persistence.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from intelligence.domain.entities import UserAbilityEntity


class AbilityRepositoryPort(ABC):
    """Abstract port for UserAbilityProfile persistence."""

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[UserAbilityEntity]:
        ...

    @abstractmethod
    def save(self, profile: UserAbilityEntity) -> UserAbilityEntity:
        ...

    @abstractmethod
    def list_top_users(self, limit: int = 100) -> List[UserAbilityEntity]:
        ...
