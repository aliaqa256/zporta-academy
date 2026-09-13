"""
ElevenLabs TTS Provider Adapter.
"""
import time
from ai_core.domain.entities import TTSRequestEntity, TTSResponseEntity
from ai_core.application.ports.outbound.tts_provider_port import TTSProviderPort
from ai_core.domain.policies import CostEstimationPolicy


class ElevenLabsTTSAdapter(TTSProviderPort):
    @property
    def provider_name(self) -> str:
        return "elevenlabs"

    def synthesize(self, request: TTSRequestEntity) -> TTSResponseEntity:
        start_time = time.time()
        from dailycast.services_interactive import _synthesize_with_elevenlabs
        audio_bytes, voice_id = _synthesize_with_elevenlabs(request.text, request.language)
        latency_ms = int((time.time() - start_time) * 1000)
        cost_estimate = CostEstimationPolicy.estimate_tts_cost("elevenlabs", len(request.text))

        return TTSResponseEntity(
            audio_bytes=audio_bytes,
            provider="elevenlabs",
            voice_id=voice_id or request.voice_id or "default",
            duration_sec=len(audio_bytes) / 32000.0,
            cost_estimate=cost_estimate,
            latency_ms=latency_ms
        )
