"""
DailyCast Repository Port Interface.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dailycast.domain.entities import DailyPodcastEntity


class DailyCastRepositoryPort(ABC):
    """Outbound port for persisting and querying daily podcasts and user learning stats."""

    @abstractmethod
    def get_by_id(self, podcast_id: int) -> Optional[DailyPodcastEntity]:
        """Retrieve a podcast by primary key."""
        pass

    @abstractmethod
    def list_for_user(self, user_id: int, is_staff: bool = False) -> List[DailyPodcastEntity]:
        """List podcasts visible to the given user."""
        pass

    @abstractmethod
    def save(self, podcast: DailyPodcastEntity, audio_bytes: Optional[bytes] = None, audio_bytes_secondary: Optional[bytes] = None) -> DailyPodcastEntity:
        """Persist or update a podcast entity."""
        pass

    @abstractmethod
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Collect aggregated learning analytics for a user."""
        pass

    @abstractmethod
    def check_recent_podcast_within_hours(self, user_id: int, hours: int = 24) -> Optional[DailyPodcastEntity]:
        """Check if user completed a podcast within the last N hours."""
        pass
