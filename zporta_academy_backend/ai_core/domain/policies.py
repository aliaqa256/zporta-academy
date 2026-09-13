"""
Domain policies for AI prompt hashing, provider selection, and cost estimation.
Zero framework dependencies.
"""
import hashlib
import json
from typing import Dict, Any, Tuple, Optional
from .value_objects import ModelTier, RequestType


class PromptHashPolicy:
    """Computes deterministic SHA256 hashes for prompt caching."""

    @staticmethod
    def compute_hash(request_type: str, prompt_text: str, options: Optional[Dict[str, Any]] = None) -> str:
        normalized_prompt = " ".join(prompt_text.strip().split())
        normalized_options = json.dumps(options or {}, sort_keys=True)
        combined = f"{request_type}|{normalized_prompt}|{normalized_options}"
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()


class ProviderSelectionPolicy:
    """Selects appropriate model tier and default provider/model."""

    @staticmethod
    def determine_tier(request_type: str, options: Optional[Dict[str, Any]] = None) -> str:
        options = options or {}
        if options.get("quality") == "premium" or options.get("deep_reasoning"):
            return ModelTier.PREMIUM.value
        if request_type in ["podcast_script", "report", "lesson_script"]:
            return ModelTier.NORMAL.value
        return ModelTier.CHEAP.value

    @staticmethod
    def default_model_for_tier(tier: str) -> Tuple[str, str]:
        if tier == ModelTier.PREMIUM.value:
            return "openai", "gpt-4o"
        elif tier == ModelTier.NORMAL.value:
            return "gemini", "gemini-1.5-flash"
        return "openai", "gpt-4o-mini"

    @staticmethod
    def default_tts_provider(has_elevenlabs_key: bool = False) -> str:
        if has_elevenlabs_key:
            return "elevenlabs"
        return "openai"


class CostEstimationPolicy:
    """Calculates approximate API costs in USD."""

    # Default rates per million tokens
    RATES_PER_1M = {
        "gpt-4o-mini": 0.15,
        "gpt-4o": 2.50,
        "gemini-1.5-flash": 0.075,
        "gemini-1.5-pro": 1.25,
        "claude-3-5-haiku": 0.80,
    }

    @classmethod
    def estimate_text_cost(cls, model_name: str, tokens_used: int) -> float:
        rate = cls.RATES_PER_1M.get(model_name, 0.15)
        return round((tokens_used / 1_000_000.0) * rate, 6)

    @classmethod
    def estimate_tts_cost(cls, provider: str, char_count: int) -> float:
        if provider == "elevenlabs":
            return round(char_count * 0.000015, 6)
        elif provider == "openai":
            return round(char_count * 0.000015, 6)
        elif provider == "google_tts":
            return round(char_count * 0.000004, 6)
        return 0.0
