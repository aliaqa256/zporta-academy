"""
AI Core Domain package.
Zero Django dependencies.
"""
from .entities import (
    LLMRequestEntity,
    LLMResponseEntity,
    TTSRequestEntity,
    TTSResponseEntity,
    AiMemoryEntity,
    AiProviderConfigEntity,
    AiUsageLogEntity
)
from .value_objects import ModelProvider, ModelTier, RequestType, SelectionMode
from .policies import ProviderSelectionPolicy, PromptHashPolicy, CostEstimationPolicy
from .exceptions import (
    AIProviderError,
    AIProviderUnavailableError,
    AIQuotaExceededError,
    InvalidAIRequestError
)

__all__ = [
    "LLMRequestEntity",
    "LLMResponseEntity",
    "TTSRequestEntity",
    "TTSResponseEntity",
    "AiMemoryEntity",
    "AiProviderConfigEntity",
    "AiUsageLogEntity",
    "ModelProvider",
    "ModelTier",
    "RequestType",
    "SelectionMode",
    "ProviderSelectionPolicy",
    "PromptHashPolicy",
    "CostEstimationPolicy",
    "AIProviderError",
    "AIProviderUnavailableError",
    "AIQuotaExceededError",
    "InvalidAIRequestError",
]
