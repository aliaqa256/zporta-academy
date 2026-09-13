"""
Learning Repository Outbound Port Interface.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from learning.domain.entities import LearningRecordEntity, StudyDashboardEntity, StudyItemEntity


class LearningRepositoryPort(ABC):
    """Outbound port for learning records, dashboard aggregates, and spaced repetition items."""

    @abstractmethod
    def get_user_learning_records(self, user_id: int) -> List[LearningRecordEntity]:
        """Fetch all learning records for a specific user."""
        pass

    @abstractmethod
    def get_dashboard_aggregates(self, user_id: int, limit: int = 5, request_context: Optional[Dict[str, Any]] = None) -> StudyDashboardEntity:
        """Fetch personalized learning dashboard aggregate recommendations."""
        pass

    @abstractmethod
    def get_study_item(self, item_id: int) -> Optional[StudyItemEntity]:
        """Fetch a specific spaced repetition study item."""
        pass

    @abstractmethod
    def save_study_item(self, item: StudyItemEntity) -> StudyItemEntity:
        """Persist updated spaced repetition study item."""
        pass
