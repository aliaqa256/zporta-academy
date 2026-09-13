"""
Composition Root for AI Core Domain.
Constructs use cases with concrete adapters.
"""
from django.conf import settings
from ai_core.adapters.outbound.persistence.django_ai_repository import (
    DjangoAiMemoryRepository,
    DjangoAiUsageLogRepository,
    DjangoAiProviderConfigRepository
)
from ai_core.adapters.outbound.providers.openai_adapter import OpenAILLMAdapter
from ai_core.adapters.outbound.providers.gemini_adapter import GeminiLLMAdapter
from ai_core.adapters.outbound.providers.claude_adapter import ClaudeLLMAdapter
from ai_core.adapters.outbound.providers.elevenlabs_tts_adapter import ElevenLabsTTSAdapter
from ai_core.adapters.outbound.providers.google_tts_adapter import GoogleTTSAdapter
from ai_core.application.use_cases.generate_text import GenerateTextUseCase
from ai_core.application.use_cases.generate_audio import GenerateAudioUseCase


def build_ai_memory_repository() -> DjangoAiMemoryRepository:
    return DjangoAiMemoryRepository()


def build_ai_usage_log_repository() -> DjangoAiUsageLogRepository:
    return DjangoAiUsageLogRepository()


def build_ai_provider_config_repository() -> DjangoAiProviderConfigRepository:
    return DjangoAiProviderConfigRepository()


def build_generate_text_use_case() -> GenerateTextUseCase:
    providers = {
        "openai": OpenAILLMAdapter(),
        "gemini": GeminiLLMAdapter(),
        "claude": ClaudeLLMAdapter(),
    }
    return GenerateTextUseCase(
        providers=providers,
        memory_repo=build_ai_memory_repository(),
        usage_log_repo=build_ai_usage_log_repository(),
        config_repo=build_ai_provider_config_repository()
    )


def build_generate_audio_use_case() -> GenerateAudioUseCase:
    tts_providers = {
        "elevenlabs": ElevenLabsTTSAdapter(),
        "google_tts": GoogleTTSAdapter(),
    }
    has_elevenlabs = bool(getattr(settings, "ELEVENLABS_API_KEY", None))
    return GenerateAudioUseCase(
        tts_providers=tts_providers,
        memory_repo=build_ai_memory_repository(),
        usage_log_repo=build_ai_usage_log_repository(),
        has_elevenlabs_key=has_elevenlabs
    )
