"""
DailyCast Application DTOs.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class GeneratePodcastCommand:
    """Command payload for initiating a podcast generation."""
    user_id: int
    primary_language: str = "en"
    secondary_language: str = ""
    output_format: str = "both"
    month_range: str = "current"
    reply_size: str = "medium"
    category: str = ""
    topic: str = ""
    profession: str = ""
    notes: str = ""
    request_data: Dict[str, Any] = field(default_factory=dict)
    requested_by_id: Optional[int] = None
    request_type: str = "user"


@dataclass(frozen=True)
class SubmitAnswersCommand:
    """Command payload for submitting student answers to podcast questions."""
    podcast_id: int
    user_id: int
    answers: Dict[str, str]
    is_staff: bool = False


@dataclass(frozen=True)
class PodcastSummaryDTO:
    id: int
    user_id: int
    primary_language: str
    secondary_language: str
    output_format: str
    status: str
    duration_seconds: int
    created_at: Optional[datetime] = None


@dataclass(frozen=True)
class PodcastDetailDTO:
    id: int
    user_id: int
    username: str
    primary_language: str
    secondary_language: str
    output_format: str
    month_range: str
    reply_size: str
    included_courses: List[Dict[str, Any]]
    category: str
    topic: str
    profession: str
    notes: str
    script_text: str
    questions_asked: List[str]
    student_answers: Dict[str, str]
    audio_file_url: Optional[str]
    audio_file_secondary_url: Optional[str]
    llm_provider: str
    tts_provider: str
    duration_seconds: int
    duration_seconds_secondary: int
    status: str
    error_message: Optional[str]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass(frozen=True)
class AccuracyCheckResultDTO:
    status: str
    accuracy_score: float
    issues: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]
    content_checks: Dict[str, Any]
    recommendation: str


@dataclass(frozen=True)
class StudentProgressDTO:
    status: str
    podcast_info: Dict[str, Any]
    progress: Dict[str, Any]
    questions: List[Dict[str, Any]]
    engagement: Dict[str, Any]
    recommendation: str


@dataclass(frozen=True)
class ScriptGenerationResultDTO:
    script_text: str
    llm_provider: str
    questions: List[str]
    duration_seconds: int
