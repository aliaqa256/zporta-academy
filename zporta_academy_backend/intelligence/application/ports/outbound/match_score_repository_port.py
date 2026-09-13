"""
Outbound Port interface for MatchScore persistence and recommendations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from intelligence.domain.entities import MatchScoreEntity


class MatchScoreRepositoryPort(ABC):
    """Abstract port for MatchScore queries and updates."""

    @abstractmethod
    def get_top_matches_for_user(
        self,
        user_id: int,
        content_type: str = "quiz",
        limit: int = 20
    ) -> List[MatchScoreEntity]:
        ...

    @abstractmethod
    def save_match_scores(self, match_scores: List[MatchScoreEntity]) -> None:
        ...
