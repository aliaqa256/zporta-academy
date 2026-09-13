from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Tuple
from ai_core.domain.entities import AiMemoryEntity


class AiMemoryRepositoryPort(ABC):
    """Abstract port for querying and updating AI memory cache."""

    @abstractmethod
    def get_by_hash(self, request_type: str, prompt_hash: str) -> Optional[AiMemoryEntity]:
        ...

    @abstractmethod
    def save_text_response(
        self,
        request_type: str,
        prompt_hash: str,
        prompt_text: str,
        prompt_options: Dict[str, Any],
        generated_text: str,
        provider: str,
        model: str,
        tokens_used: int,
        cost_estimate: float,
        latency_ms: int
    ) -> AiMemoryEntity:
        ...

    @abstractmethod
    def save_audio_response(
        self,
        text_hash: str,
        text: str,
        audio_bytes: bytes,
        provider: str,
        language: str,
        voice_id: str,
        cost_estimate: float,
        latency_ms: int
    ) -> AiMemoryEntity:
        ...

    @abstractmethod
    def get_audio_by_hash(self, text_hash: str) -> Optional[Tuple[bytes, AiMemoryEntity]]:
        ...
