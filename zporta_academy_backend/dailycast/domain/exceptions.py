"""
DailyCast Domain Exceptions.
"""
from core.shared_kernel.domain.exceptions import DomainException, EntityNotFoundError


class DailycastError(DomainException):
    """Base exception for all DailyCast domain errors."""
    pass


class DailyPodcastNotFoundError(EntityNotFoundError):
    """Raised when a podcast entity cannot be found."""
    def __init__(self, podcast_id: int):
        super().__init__(f"DailyPodcast with ID {podcast_id} was not found.")
        self.podcast_id = podcast_id


class DailycastCooldownError(DailycastError):
    """Raised when a generation request violates the 24-hour cooldown policy."""
    pass


class InvalidScriptFormatError(DailycastError):
    """Raised when a generated or input script does not satisfy format invariants."""
    pass


class AudioSynthesisError(DailycastError):
    """Raised when TTS or audio stitching fails."""
    pass
