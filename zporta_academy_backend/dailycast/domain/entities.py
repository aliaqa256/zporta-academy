"""
DailyCast Domain Entities.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from core.shared_kernel.domain.base_entity import BaseEntity
from dailycast.domain.value_objects import MonthRange, OutputFormat, PodcastStatus, ReplySize


@dataclass(frozen=True)
class ScriptSegment:
    """Represents a structured section of a podcast script."""
    speaker: str
    text: str
    timing_tag: Optional[str] = None
    emphasis: bool = False


@dataclass
class PodcastScriptEntity:
    """Represents a generated podcast script."""
    raw_text: str
    language: str
    segments: List[ScriptSegment] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)
    word_count: int = 0
    motivational_quote: Optional[str] = None


@dataclass
class AudioTrackEntity:
    """Represents synthesized audio bytes and metadata."""
    audio_bytes: bytes
    duration_seconds: int
    provider: str
    format: str = "mp3"
    language: str = "en"


@dataclass(eq=False)
class DailyPodcastEntity(BaseEntity[Optional[int]]):
    """Core domain entity representing a personalized learning podcast."""
    id: Optional[int] = None
    user_id: int = 0
    primary_language: str = "en"
    secondary_language: str = ""
    output_format: OutputFormat = OutputFormat.BOTH
    month_range: MonthRange = MonthRange.CURRENT
    reply_size: ReplySize = ReplySize.MEDIUM
    included_courses: List[Dict[str, Any]] = field(default_factory=list)
    category: str = ""
    topic: str = ""
    profession: str = ""
    notes: str = ""
    request_data: Dict[str, Any] = field(default_factory=dict)
    
    script_text: str = ""
    questions_asked: List[str] = field(default_factory=list)
    student_answers: Dict[str, str] = field(default_factory=dict)
    
    audio_file_url: Optional[str] = None
    audio_file_secondary_url: Optional[str] = None
    llm_provider: str = "template"
    tts_provider: str = "polly"
    duration_seconds: int = 0
    duration_seconds_secondary: int = 0
    status: PodcastStatus = PodcastStatus.PENDING
    error_message: Optional[str] = None
    
    requested_by_user: bool = False
    requested_by_id: Optional[int] = None
    user_request_type: str = "user"
    can_request_again_at: Optional[datetime] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_completed(self) -> bool:
        return self.status == PodcastStatus.COMPLETED

    def is_failed(self) -> bool:
        return self.status == PodcastStatus.FAILED

    def mark_completed(self, script_text: str, duration_seconds: int, llm_provider: str, tts_provider: str) -> None:
        self.script_text = script_text
        self.duration_seconds = duration_seconds
        self.llm_provider = llm_provider
        self.tts_provider = tts_provider
        self.status = PodcastStatus.COMPLETED
        self.error_message = None

    def mark_failed(self, error_message: str) -> None:
        self.status = PodcastStatus.FAILED
        self.error_message = error_message
        if not self.script_text:
            self.script_text = "Podcast generation failed before script was saved."
