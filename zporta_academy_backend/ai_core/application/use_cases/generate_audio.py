"""
Use Case: Generate Audio via TTS Providers with caching and usage tracking.
"""
import time
from typing import Optional, Dict
from core.shared_kernel.domain.result import Result, ok, err
from ai_core.domain.entities import TTSRequestEntity, TTSResponseEntity, AiUsageLogEntity
from ai_core.domain.policies import PromptHashPolicy, ProviderSelectionPolicy, CostEstimationPolicy
from ai_core.domain.exceptions import AIProviderError, AIProviderUnavailableError
from ai_core.application.dtos import GenerateAudioCommand, AudioGenerationResultDTO
from ai_core.application.ports.outbound.tts_provider_port import TTSProviderPort
from ai_core.application.ports.outbound.ai_memory_repository_port import AiMemoryRepositoryPort
from ai_core.application.ports.outbound.ai_usage_log_port import AiUsageLogRepositoryPort


class GenerateAudioUseCase:
    def __init__(
        self,
        tts_providers: Dict[str, TTSProviderPort],
        memory_repo: AiMemoryRepositoryPort,
        usage_log_repo: AiUsageLogRepositoryPort,
        has_elevenlabs_key: bool = False
    ):
        self._tts_providers = tts_providers
        self._memory_repo = memory_repo
        self._usage_log_repo = usage_log_repo
        self._has_elevenlabs_key = has_elevenlabs_key

    def execute(self, cmd: GenerateAudioCommand) -> Result[AudioGenerationResultDTO, Exception]:
        start_time = time.time()
        options = {"language": cmd.language, "voice_id": cmd.voice_id}

        # 1. Check audio cache (unless force_refresh)
        text_hash = PromptHashPolicy.compute_hash("tts_audio", cmd.text, options)
        if not cmd.force_refresh:
            cached = self._memory_repo.get_audio_by_hash(text_hash)
            if cached:
                audio_bytes, memory_item = cached
                latency_ms = int((time.time() - start_time) * 1000)

                self._usage_log_repo.log_usage(
                    AiUsageLogEntity(
                        request_type="tts_audio",
                        endpoint=cmd.endpoint,
                        user_id=cmd.user_id,
                        provider=memory_item.provider,
                        model=memory_item.model or cmd.voice_id or "default",
                        tokens_used=0,
                        cost_estimate=memory_item.cost_estimate,
                        latency_ms=latency_ms,
                        cache_hit=True,
                        memory_id=memory_item.id,
                        selection_mode=cmd.selection_mode
                    )
                )

                dto = AudioGenerationResultDTO(
                    audio_bytes=audio_bytes,
                    provider_used=memory_item.provider,
                    voice_id=memory_item.model or cmd.voice_id or "default",
                    cost_estimate=memory_item.cost_estimate or 0.0,
                    latency_ms=latency_ms,
                    cache_hit=True
                )
                return ok(dto)

        # 2. Select TTS provider
        provider_name = cmd.provider
        if cmd.selection_mode == "auto" or not provider_name:
            provider_name = ProviderSelectionPolicy.default_tts_provider(self._has_elevenlabs_key)

        provider_adapter = self._tts_providers.get(provider_name)
        if not provider_adapter:
            # Fallback to any available provider
            for fallback_name, adapter in self._tts_providers.items():
                if adapter:
                    provider_adapter = adapter
                    provider_name = fallback_name
                    break

        if not provider_adapter:
            return err(AIProviderUnavailableError(provider_name or "default"))

        tts_req = TTSRequestEntity(
            text=cmd.text,
            language=cmd.language,
            voice_id=cmd.voice_id,
            provider=provider_name
        )

        try:
            tts_res = provider_adapter.synthesize(tts_req)
            latency_ms = int((time.time() - start_time) * 1000)

            # 3. Save to audio memory
            saved_memory = self._memory_repo.save_audio_response(
                text_hash=text_hash,
                text=cmd.text,
                audio_bytes=tts_res.audio_bytes,
                provider=tts_res.provider,
                language=cmd.language,
                voice_id=tts_res.voice_id,
                cost_estimate=tts_res.cost_estimate,
                latency_ms=latency_ms
            )

            # 4. Log usage
            self._usage_log_repo.log_usage(
                AiUsageLogEntity(
                    request_type="tts_audio",
                    endpoint=cmd.endpoint,
                    user_id=cmd.user_id,
                    provider=tts_res.provider,
                    model=tts_res.voice_id,
                    tokens_used=0,
                    cost_estimate=tts_res.cost_estimate,
                    latency_ms=latency_ms,
                    cache_hit=False,
                    memory_id=saved_memory.id,
                    selection_mode=cmd.selection_mode,
                    success=True
                )
            )

            dto = AudioGenerationResultDTO(
                audio_bytes=tts_res.audio_bytes,
                provider_used=tts_res.provider,
                voice_id=tts_res.voice_id,
                cost_estimate=tts_res.cost_estimate,
                latency_ms=latency_ms,
                cache_hit=False
            )
            return ok(dto)

        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            self._usage_log_repo.log_usage(
                AiUsageLogEntity(
                    request_type="tts_audio",
                    endpoint=cmd.endpoint,
                    user_id=cmd.user_id,
                    provider=provider_name or "unknown",
                    model=cmd.voice_id or "default",
                    tokens_used=0,
                    cost_estimate=0.0,
                    latency_ms=latency_ms,
                    cache_hit=False,
                    selection_mode=cmd.selection_mode,
                    success=False,
                    error_message=str(e)
                )
            )
            return err(AIProviderError(str(e)))
