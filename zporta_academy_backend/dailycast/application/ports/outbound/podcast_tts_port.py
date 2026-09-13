"""
Podcast TTS Provider Port.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dailycast.domain.entities import AudioTrackEntity


class PodcastTTSPort(ABC):
    """Outbound port for synthesizing spoken audio from script text."""

    @abstractmethod
    def synthesize(self, script_text: str, language: str, voice_config: Optional[Dict[str, Any]] = None) -> AudioTrackEntity:
        """Synthesize script into an audio track entity."""
        pass
