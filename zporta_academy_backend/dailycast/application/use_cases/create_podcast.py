"""
Create Podcast Use Case.
"""
import logging
from typing import Optional

from dailycast.application.dtos.podcast_dtos import GeneratePodcastCommand, PodcastDetailDTO
from dailycast.application.ports.outbound.dailycast_repository_port import DailyCastRepositoryPort
from dailycast.application.ports.outbound.podcast_tts_port import PodcastTTSPort
from dailycast.domain.entities import DailyPodcastEntity
from dailycast.domain.exceptions import DailycastCooldownError
from dailycast.domain.policies import ProficiencyEvaluationPolicy, ScriptValidationPolicy
from dailycast.domain.value_objects import MonthRange, OutputFormat, PodcastStatus, ReplySize

logger = logging.getLogger(__name__)


class CreatePodcastUseCase:
    """Use case to generate, synthesize, and persist a personalized learning podcast."""

    def __init__(
        self,
        repository: DailyCastRepositoryPort,
        tts_provider: Optional[PodcastTTSPort] = None,
        enforce_cooldown: bool = False,
    ):
        self.repository = repository
        self.tts_provider = tts_provider
        self.enforce_cooldown = enforce_cooldown

    def execute(self, request: GeneratePodcastCommand) -> PodcastDetailDTO:
        # 1. Cooldown validation if enabled
        if self.enforce_cooldown:
            recent = self.repository.check_recent_podcast_within_hours(request.user_id, hours=24)
            if recent and recent.created_at:
                raise DailycastCooldownError(
                    f"Podcast already generated for user {request.user_id}. Please wait 24 hours."
                )

        # 2. Gather learner statistics
        user_stats = self.repository.get_user_stats(request.user_id)

        # 3. Create initial pending entity
        podcast = DailyPodcastEntity(
            user_id=request.user_id,
            primary_language=request.primary_language or "en",
            secondary_language=request.secondary_language or "",
            output_format=OutputFormat(request.output_format) if request.output_format in OutputFormat._value2member_map_ else OutputFormat.BOTH,
            month_range=MonthRange(request.month_range) if request.month_range in MonthRange._value2member_map_ else MonthRange.CURRENT,
            reply_size=ReplySize(request.reply_size) if request.reply_size in ReplySize._value2member_map_ else ReplySize.MEDIUM,
            category=request.category,
            topic=request.topic,
            profession=request.profession,
            notes=request.notes,
            request_data=request.request_data,
            requested_by_user=request.requested_by_id is not None,
            requested_by_id=request.requested_by_id,
            user_request_type=request.request_type,
            status=PodcastStatus.PENDING,
            included_courses=user_stats.get("enrolled_courses", []),
        )

        # 4. Generate script (fallback template or LLM service)
        ability_level = user_stats.get("ability_level") or "steady"
        weak_subject = user_stats.get("weak_subject") or "general refresher concepts"
        username = user_stats.get("username", "Learner")

        script_text = (
            f"Hey {username}, welcome back to your daily learning podcast! "
            f"You are currently progressing at a {ability_level} level. "
            f"Today, let's explore {weak_subject}. "
            "First, remember that consistent practice beats intensity every single time. "
            "Second, try reviewing your recent notes before tackling the next quiz module. "
            "Here is a question for you: How do you plan to apply what you learned today in your next study session? "
            "Keep pushing forward and stay curious!"
        )
        llm_provider = "template"

        # Extract interactive questions
        questions = ScriptValidationPolicy.extract_questions(script_text)
        if not questions:
            questions = ["How do you plan to apply what you learned today in your next study session?"]

        duration_sec = ProficiencyEvaluationPolicy.estimate_duration_seconds(script_text)
        podcast.script_text = script_text
        podcast.questions_asked = questions
        podcast.llm_provider = llm_provider
        podcast.duration_seconds = duration_sec

        # 5. Synthesize Audio if requested
        primary_audio_bytes = None
        tts_provider_name = "none"

        if podcast.output_format in [OutputFormat.AUDIO, OutputFormat.BOTH] and self.tts_provider:
            try:
                audio_track = self.tts_provider.synthesize(script_text, podcast.primary_language)
                primary_audio_bytes = audio_track.audio_bytes
                tts_provider_name = audio_track.provider
                if audio_track.duration_seconds > 0:
                    podcast.duration_seconds = audio_track.duration_seconds
            except Exception as e:
                logger.warning(f"DailyCast TTS synthesis warning: {e}")
                tts_provider_name = "none"

        podcast.tts_provider = tts_provider_name
        podcast.status = PodcastStatus.COMPLETED

        # 6. Save via repository port
        saved = self.repository.save(podcast, audio_bytes=primary_audio_bytes)

        return PodcastDetailDTO(
            id=saved.id or 0,
            user_id=saved.user_id,
            username=username,
            primary_language=saved.primary_language,
            secondary_language=saved.secondary_language,
            output_format=saved.output_format.value,
            month_range=saved.month_range.value,
            reply_size=saved.reply_size.value,
            included_courses=saved.included_courses,
            category=saved.category,
            topic=saved.topic,
            profession=saved.profession,
            notes=saved.notes,
            script_text=saved.script_text,
            questions_asked=saved.questions_asked,
            student_answers=saved.student_answers,
            audio_file_url=saved.audio_file_url,
            audio_file_secondary_url=saved.audio_file_secondary_url,
            llm_provider=saved.llm_provider,
            tts_provider=saved.tts_provider,
            duration_seconds=saved.duration_seconds,
            duration_seconds_secondary=saved.duration_seconds_secondary,
            status=saved.status.value,
            error_message=saved.error_message,
            created_at=saved.created_at,
            updated_at=saved.updated_at,
        )
