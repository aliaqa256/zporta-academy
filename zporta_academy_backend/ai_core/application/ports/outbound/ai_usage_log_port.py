"""
Outbound Port interface for AI Usage logging.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ai_core.domain.entities import AiUsageLogEntity


class AiUsageLogRepositoryPort(ABC):
    """Abstract port for tracking AI calls and costs."""

    @abstractmethod
    def log_usage(self, entry: AiUsageLogEntity) -> None:
        ...

    @abstractmethod
    def get_cost_summary(self, days: int = 30) -> Dict[str, Any]:
        ...
