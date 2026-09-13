from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import date
from gamification.domain.entities import ActivityEntity, UserScoreEntity


class GamificationRepositoryPort(ABC):
    """Abstract port for gamification activity and user score persistence."""

    @abstractmethod
    def log_activity(
        self,
        user_id: int,
        activity_type: str,
        points: int,
        unique_key: str,
        is_mistake: bool = False,
        metadata: dict = None,
        time_spent_seconds: Optional[int] = None
    ) -> Optional[ActivityEntity]:
        pass

    @abstractmethod
    def get_or_create_user_score(self, user_id: int) -> UserScoreEntity:
        pass

    @abstractmethod
    def recalculate_user_score(self, user_id: int) -> UserScoreEntity:
        pass

    @abstractmethod
    def get_user_activity_dates(self, user_id: int, days_limit: int = 365) -> List[date]:
        pass
