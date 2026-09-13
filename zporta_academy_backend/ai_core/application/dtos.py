"""
Application Layer DTOs for AI Core.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass(frozen=True)
class GenerateTextCommand:
    request_type: str
    prompt: str
    options: Dict[str, Any] = field(default_factory=dict)
    provider: Optional[str] = None
    model: Optional[str] = None
    selection_mode: str = "auto"
    user_id: Optional[int] = None
    endpoint: str = "unknown"
    force_refresh: bool = False


@dataclass(frozen=True)
class TextGenerationResultDTO:
    generated_text: str
    provider_used: str
    model_used: str
    tokens_used: int
    cost_estimate: float
    latency_ms: int
    cache_hit: bool


@dataclass(frozen=True)
class GenerateAudioCommand:
    text: str
    language: str = "en"
    provider: Optional[str] = None
    voice_id: Optional[str] = None
    selection_mode: str = "auto"
    user_id: Optional[int] = None
    endpoint: str = "unknown"
    force_refresh: bool = False


@dataclass(frozen=True)
class AudioGenerationResultDTO:
    audio_bytes: bytes
    provider_used: str
    voice_id: str
    cost_estimate: float
    latency_ms: int
    cache_hit: bool


@dataclass(frozen=True)
class CostSummaryDTO:
    total_requests: int
    total_cost: float
    total_tokens: int
    cache_hit_rate: float
    by_provider: List[Dict[str, Any]] = field(default_factory=list)
