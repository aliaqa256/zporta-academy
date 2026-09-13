"""
DailyCast Pydub Audio Stitcher Adapter.
"""
import io
import logging
from typing import List
from dailycast.application.ports.outbound.podcast_stitcher_port import PodcastStitcherPort
from dailycast.domain.entities import AudioTrackEntity

logger = logging.getLogger(__name__)


class PydubAudioStitcherAdapter(PodcastStitcherPort):
    """Combines multiple audio tracks using pydub."""

    def stitch_tracks(self, tracks: List[AudioTrackEntity], crossfade_ms: int = 100) -> AudioTrackEntity:
        if not tracks:
            return AudioTrackEntity(audio_bytes=b"", duration_seconds=0, provider="pydub")

        if len(tracks) == 1:
            return tracks[0]

        valid_tracks = [t for t in tracks if t.audio_bytes]
        if not valid_tracks:
            total_dur = sum(t.duration_seconds for t in tracks)
            return AudioTrackEntity(audio_bytes=b"", duration_seconds=total_dur, provider="pydub")

        try:
            from pydub import AudioSegment

            combined = None
            for track in valid_tracks:
                seg = AudioSegment.from_file(io.BytesIO(track.audio_bytes), format="mp3")
                if combined is None:
                    combined = seg
                else:
                    if crossfade_ms > 0 and len(combined) > crossfade_ms and len(seg) > crossfade_ms:
                        combined = combined.append(seg, crossfade=crossfade_ms)
                    else:
                        combined = combined + seg

            out_io = io.BytesIO()
            combined.export(out_io, format="mp3")
            out_bytes = out_io.getvalue()
            duration_sec = int(len(combined) / 1000)

            return AudioTrackEntity(
                audio_bytes=out_bytes,
                duration_seconds=duration_sec,
                provider="pydub",
            )
        except Exception as e:
            logger.warning(f"Audio stitching fallback to concatenation due to: {e}")
            concatenated = b"".join(t.audio_bytes for t in valid_tracks)
            total_duration = sum(t.duration_seconds for t in valid_tracks)
            return AudioTrackEntity(
                audio_bytes=concatenated,
                duration_seconds=total_duration,
                provider="fallback",
            )
