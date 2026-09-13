"""
DailyCast Polly and Multi-Provider TTS Adapter.
"""
import logging
from typing import Any, Dict, Optional, Tuple
from django.conf import settings
from dailycast.application.ports.outbound.podcast_tts_port import PodcastTTSPort
from dailycast.domain.entities import AudioTrackEntity
from dailycast.domain.policies import ProficiencyEvaluationPolicy

logger = logging.getLogger(__name__)


class PollyTTSAdapter(PodcastTTSPort):
    """Synthesizes speech using Amazon Polly with graceful fallback."""

    def _pick_polly_voice(self, language: str) -> Tuple[str, str]:
        lang = (language or "en").lower()
        if lang.startswith("ja"):
            return "Mizuki", "neural"
        if lang.startswith("es"):
            return "Lucia", "neural"
        if lang.startswith("fr"):
            return "Celine", "neural"
        if lang.startswith("de"):
            return "Vicki", "neural"
        return "Joanna", "neural"

    def synthesize(
        self,
        script_text: str,
        language: str,
        voice_config: Optional[Dict[str, Any]] = None,
    ) -> AudioTrackEntity:
        aws_key = getattr(settings, "AWS_ACCESS_KEY_ID", None)
        aws_secret = getattr(settings, "AWS_SECRET_ACCESS_KEY", None)

        duration_est = ProficiencyEvaluationPolicy.estimate_duration_seconds(script_text)

        if not aws_key or not aws_secret:
            logger.info("DailyCast Polly TTS skipped: AWS credentials not configured.")
            return AudioTrackEntity(
                audio_bytes=b"",
                duration_seconds=duration_est,
                provider="none",
                language=language,
            )

        voice_id, engine = self._pick_polly_voice(language)
        try:
            import boto3
            polly = boto3.client(
                "polly",
                region_name=getattr(settings, "AWS_REGION", "us-east-1"),
                aws_access_key_id=aws_key,
                aws_secret_access_key=aws_secret,
            )
            response = polly.synthesize_speech(
                Text=script_text[:4500],
                OutputFormat="mp3",
                VoiceId=voice_id,
                Engine=engine,
            )
            audio_stream = response.get("AudioStream")
            if not audio_stream:
                raise ValueError("Polly returned no audio stream")
            audio_bytes = audio_stream.read()
            return AudioTrackEntity(
                audio_bytes=audio_bytes,
                duration_seconds=duration_est,
                provider="polly",
                language=language,
            )
        except Exception as exc:
            logger.warning(f"DailyCast Polly synthesis error: {exc}")
            return AudioTrackEntity(
                audio_bytes=b"",
                duration_seconds=duration_est,
                provider="none",
                language=language,
            )
