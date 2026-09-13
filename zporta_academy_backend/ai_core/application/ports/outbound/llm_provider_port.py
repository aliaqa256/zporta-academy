"""
Outbound Port interface for Large Language Model providers.
"""
from abc import ABC, abstractmethod
from ai_core.domain.entities import LLMRequestEntity, LLMResponseEntity


class LLMProviderPort(ABC):
    """Abstract port for text generation providers."""

    @abstractmethod
    def generate(self, request: LLMRequestEntity) -> LLMResponseEntity:
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...
