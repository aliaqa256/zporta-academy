"""
Outbound Port interface for Text-To-Speech providers.
"""
from abc import ABC, abstractmethod
from ai_core.domain.entities import TTSRequestEntity, TTSResponseEntity


class TTSProviderPort(ABC):
    """Abstract port for speech synthesis providers."""

    @abstractmethod
    def synthesize(self, request: TTSRequestEntity) -> TTSResponseEntity:
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...
