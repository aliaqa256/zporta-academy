"""
Podcast Audio Stitcher Port.
"""
from abc import ABC, abstractmethod
from typing import List
from dailycast.domain.entities import AudioTrackEntity


class PodcastStitcherPort(ABC):
    """Outbound port for concatenating multiple audio tracks, intros, and background jingles."""

    @abstractmethod
    def stitch_tracks(self, tracks: List[AudioTrackEntity], crossfade_ms: int = 100) -> AudioTrackEntity:
        """Combine audio tracks into a unified MP3 audio track."""
        pass
