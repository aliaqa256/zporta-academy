"""
Google Cloud TTS Provider Adapter.
"""
import time
from ai_core.domain.entities import TTSRequestEntity, TTSResponseEntity
from ai_core.application.ports.outbound.tts_provider_port import TTSProviderPort
from ai_core.domain.policies import CostEstimationPolicy


class GoogleTTSAdapter(TTSProviderPort):
    @property
    def provider_name(self) -> str:
        return "google_tts"

    def synthesize(self, request: TTSRequestEntity) -> TTSResponseEntity:
        start_time = time.time()
        from dailycast.services_interactive import _synthesize_with_google_tts
        audio_bytes, voice_id = _synthesize_with_google_tts(request.text, request.language)
        latency_ms = int((time.time() - start_time) * 1000)
        cost_estimate = CostEstimationPolicy.estimate_tts_cost("google_tts", len(request.text))

        return TTSResponseEntity(
            audio_bytes=audio_bytes,
            provider="google_tts",
            voice_id=voice_id or request.voice_id or "default",
            duration_sec=len(audio_bytes) / 32000.0,
            cost_estimate=cost_estimate,
            latency_ms=latency_ms
        )
