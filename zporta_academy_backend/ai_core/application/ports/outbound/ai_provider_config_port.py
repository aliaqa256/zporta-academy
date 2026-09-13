"""
Outbound Port interface for AI Provider Configurations.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from ai_core.domain.entities import AiProviderConfigEntity


class AiProviderConfigRepositoryPort(ABC):
    """Abstract port for querying active AI provider configurations."""

    @abstractmethod
    def get_best_model_for_tier(self, tier: str) -> Optional[Tuple[str, str]]:
        ...

    @abstractmethod
    def list_active_configs(self) -> List[AiProviderConfigEntity]:
        ...
