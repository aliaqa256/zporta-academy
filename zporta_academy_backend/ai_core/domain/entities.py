"""
Pure domain entities for AI Core.
Zero Django dependencies.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from core.shared_kernel.domain.base_entity import BaseEntity
from .value_objects import ModelProvider, ModelTier, RequestType, SelectionMode


@dataclass(frozen=True)
class LLMRequestEntity:
    prompt: str
    request_type: str = "other"
    options: Dict[str, Any] = field(default_factory=dict)
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None


@dataclass(frozen=True)
class LLMResponseEntity:
    generated_text: str
    provider: str
    model: str
    tokens_used: int = 0
    cost_estimate: float = 0.0
    latency_ms: int = 0
    raw_response: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class TTSRequestEntity:
    text: str
    language: str = "en"
    voice_id: Optional[str] = None
    provider: Optional[str] = None


@dataclass(frozen=True)
class TTSResponseEntity:
    audio_bytes: bytes
    provider: str
    voice_id: str
    duration_sec: float = 0.0
    cost_estimate: float = 0.0
    latency_ms: int = 0


@dataclass(eq=False)
class AiProviderConfigEntity(BaseEntity[int]):
    id: Optional[int] = None
    provider: str = "openai"
    model_name: str = "gpt-4o-mini"
    tier: str = "normal"
    cost_per_million_tokens: Optional[float] = None
    cost_per_request: Optional[float] = None
    avg_latency_ms: Optional[int] = None
    quality_score: float = 0.8
    is_active: bool = True
    is_default: bool = False
    max_tokens: Optional[int] = None
    capabilities: Dict[str, Any] = field(default_factory=dict)


@dataclass(eq=False)
class AiMemoryEntity(BaseEntity[int]):
    id: Optional[int] = None
    request_type: str = "other"
    prompt_hash: str = ""
    prompt_text: str = ""
    prompt_options: Dict[str, Any] = field(default_factory=dict)
    generated_text: str = ""
    audio_file_path: Optional[str] = None
    audio_metadata: Dict[str, Any] = field(default_factory=dict)
    provider: str = ""
    model: str = ""
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None
    latency_ms: Optional[int] = None
    is_verified_good: bool = False
    user_rating: Optional[float] = None
    usage_count: int = 0
    use_for_training: bool = False


@dataclass(eq=False)
class AiUsageLogEntity(BaseEntity[int]):
    id: Optional[int] = None
    request_type: str = "other"
    endpoint: str = "unknown"
    user_id: Optional[int] = None
    provider: str = ""
    model: str = ""
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None
    latency_ms: int = 0
    cache_hit: bool = False
    memory_id: Optional[int] = None
    selection_mode: str = "auto"
    success: bool = True
    error_message: str = ""
    timestamp: Optional[datetime] = None
