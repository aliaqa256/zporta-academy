"""
Google Gemini LLM Provider Adapter.
"""
import time
from ai_core.domain.entities import LLMRequestEntity, LLMResponseEntity
from ai_core.application.ports.outbound.llm_provider_port import LLMProviderPort
from ai_core.domain.policies import CostEstimationPolicy


class GeminiLLMAdapter(LLMProviderPort):
    @property
    def provider_name(self) -> str:
        return "gemini"

    def generate(self, request: LLMRequestEntity) -> LLMResponseEntity:
        start_time = time.time()
        model = request.model or "gemini-1.5-flash"
        
        from dailycast.services_interactive import _call_gemini_for_text
        text, tokens_used, cost_estimate = _call_gemini_for_text(model, request.prompt, request.options)
        
        latency_ms = int((time.time() - start_time) * 1000)
        if not cost_estimate:
            cost_estimate = CostEstimationPolicy.estimate_text_cost(model, tokens_used)

        return LLMResponseEntity(
            generated_text=text,
            provider="gemini",
            model=model,
            tokens_used=tokens_used,
            cost_estimate=cost_estimate,
            latency_ms=latency_ms
        )
