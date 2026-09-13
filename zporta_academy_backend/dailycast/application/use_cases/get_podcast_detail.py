"""
Get Podcast Detail Use Case.
"""
from dailycast.application.dtos.podcast_dtos import PodcastDetailDTO
from dailycast.application.ports.outbound.dailycast_repository_port import DailyCastRepositoryPort
from dailycast.domain.exceptions import DailyPodcastNotFoundError


class GetPodcastDetailUseCase:
    """Use case to fetch details of a specific podcast."""

    def __init__(self, repository: DailyCastRepositoryPort):
        self.repository = repository

    def execute(self, podcast_id: int) -> PodcastDetailDTO:
        podcast = self.repository.get_by_id(podcast_id)
        if not podcast:
            raise DailyPodcastNotFoundError(podcast_id)

        user_stats = self.repository.get_user_stats(podcast.user_id)
        username = user_stats.get("username", f"User {podcast.user_id}")

        return PodcastDetailDTO(
            id=podcast.id or 0,
            user_id=podcast.user_id,
            username=username,
            primary_language=podcast.primary_language,
            secondary_language=podcast.secondary_language,
            output_format=podcast.output_format.value,
            month_range=podcast.month_range.value,
            reply_size=podcast.reply_size.value,
            included_courses=podcast.included_courses,
            category=podcast.category,
            topic=podcast.topic,
            profession=podcast.profession,
            notes=podcast.notes,
            script_text=podcast.script_text,
            questions_asked=podcast.questions_asked,
            student_answers=podcast.student_answers,
            audio_file_url=podcast.audio_file_url,
            audio_file_secondary_url=podcast.audio_file_secondary_url,
            llm_provider=podcast.llm_provider,
            tts_provider=podcast.tts_provider,
            duration_seconds=podcast.duration_seconds,
            duration_seconds_secondary=podcast.duration_seconds_secondary,
            status=podcast.status.value,
            error_message=podcast.error_message,
            created_at=podcast.created_at,
            updated_at=podcast.updated_at,
        )
