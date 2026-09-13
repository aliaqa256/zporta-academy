"""
Use Case: Generate Text via Multi-Provider LLM Gateway with caching and usage tracking.
"""
import time
from typing import Optional, Dict
from core.shared_kernel.domain.result import Result, ok, err
from ai_core.domain.entities import LLMRequestEntity, LLMResponseEntity, AiUsageLogEntity
from ai_core.domain.policies import PromptHashPolicy, ProviderSelectionPolicy, CostEstimationPolicy
from ai_core.domain.exceptions import AIProviderError, AIProviderUnavailableError
from ai_core.application.dtos import GenerateTextCommand, TextGenerationResultDTO
from ai_core.application.ports.outbound.llm_provider_port import LLMProviderPort
from ai_core.application.ports.outbound.ai_memory_repository_port import AiMemoryRepositoryPort
from ai_core.application.ports.outbound.ai_usage_log_port import AiUsageLogRepositoryPort
from ai_core.application.ports.outbound.ai_provider_config_port import AiProviderConfigRepositoryPort


class GenerateTextUseCase:
    def __init__(
        self,
        providers: Dict[str, LLMProviderPort],
        memory_repo: AiMemoryRepositoryPort,
        usage_log_repo: AiUsageLogRepositoryPort,
        config_repo: Optional[AiProviderConfigRepositoryPort] = None
    ):
        self._providers = providers
        self._memory_repo = memory_repo
        self._usage_log_repo = usage_log_repo
        self._config_repo = config_repo

    def execute(self, cmd: GenerateTextCommand) -> Result[TextGenerationResultDTO, Exception]:
        start_time = time.time()
        options = cmd.options or {}

        # 1. Check cache (unless force_refresh)
        prompt_hash = PromptHashPolicy.compute_hash(cmd.request_type, cmd.prompt, options)
        if not cmd.force_refresh:
            cached_memory = self._memory_repo.get_by_hash(cmd.request_type, prompt_hash)
            if cached_memory and (cached_memory.is_verified_good or (cached_memory.user_rating or 0) >= 4.0):
                latency_ms = int((time.time() - start_time) * 1000)
                
                # Log usage
                self._usage_log_repo.log_usage(
                    AiUsageLogEntity(
                        request_type=cmd.request_type,
                        endpoint=cmd.endpoint,
                        user_id=cmd.user_id,
                        provider=cached_memory.provider,
                        model=cached_memory.model,
                        tokens_used=cached_memory.tokens_used,
                        cost_estimate=cached_memory.cost_estimate,
                        latency_ms=latency_ms,
                        cache_hit=True,
                        memory_id=cached_memory.id,
                        selection_mode=cmd.selection_mode
                    )
                )

                dto = TextGenerationResultDTO(
                    generated_text=cached_memory.generated_text,
                    provider_used=cached_memory.provider,
                    model_used=cached_memory.model,
                    tokens_used=cached_memory.tokens_used or 0,
                    cost_estimate=cached_memory.cost_estimate or 0.0,
                    latency_ms=latency_ms,
                    cache_hit=True
                )
                return ok(dto)

        # 2. Select provider and model
        provider_name = cmd.provider
        model_name = cmd.model
        if cmd.selection_mode == "auto" or not (provider_name and model_name):
            tier = ProviderSelectionPolicy.determine_tier(cmd.request_type, options)
            configured_model = self._config_repo.get_best_model_for_tier(tier) if self._config_repo else None
            if configured_model:
                provider_name, model_name = configured_model
            else:
                provider_name, model_name = ProviderSelectionPolicy.default_model_for_tier(tier)

        # 3. Call LLM provider adapter
        provider_adapter = self._providers.get(provider_name)
        if not provider_adapter:
            # Fallback to default available provider (e.g. 'openai' or 'gemini')
            for fallback_name, adapter in self._providers.items():
                if adapter:
                    provider_adapter = adapter
                    provider_name = fallback_name
                    break

        if not provider_adapter:
            return err(AIProviderUnavailableError(provider_name or "default"))

        llm_request = LLMRequestEntity(
            prompt=cmd.prompt,
            request_type=cmd.request_type,
            options=options,
            provider=provider_name,
            model=model_name
        )

        try:
            llm_response = provider_adapter.generate(llm_request)
            latency_ms = int((time.time() - start_time) * 1000)

            # 4. Save to memory cache
            saved_memory = self._memory_repo.save_text_response(
                request_type=cmd.request_type,
                prompt_hash=prompt_hash,
                prompt_text=cmd.prompt,
                prompt_options=options,
                generated_text=llm_response.generated_text,
                provider=llm_response.provider,
                model=llm_response.model,
                tokens_used=llm_response.tokens_used,
                cost_estimate=llm_response.cost_estimate,
                latency_ms=latency_ms
            )

            # 5. Log usage
            self._usage_log_repo.log_usage(
                AiUsageLogEntity(
                    request_type=cmd.request_type,
                    endpoint=cmd.endpoint,
                    user_id=cmd.user_id,
                    provider=llm_response.provider,
                    model=llm_response.model,
                    tokens_used=llm_response.tokens_used,
                    cost_estimate=llm_response.cost_estimate,
                    latency_ms=latency_ms,
                    cache_hit=False,
                    memory_id=saved_memory.id,
                    selection_mode=cmd.selection_mode,
                    success=True
                )
            )

            dto = TextGenerationResultDTO(
                generated_text=llm_response.generated_text,
                provider_used=llm_response.provider,
                model_used=llm_response.model,
                tokens_used=llm_response.tokens_used,
                cost_estimate=llm_response.cost_estimate,
                latency_ms=latency_ms,
                cache_hit=False
            )
            return ok(dto)

        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            self._usage_log_repo.log_usage(
                AiUsageLogEntity(
                    request_type=cmd.request_type,
                    endpoint=cmd.endpoint,
                    user_id=cmd.user_id,
                    provider=provider_name or "unknown",
                    model=model_name or "unknown",
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
