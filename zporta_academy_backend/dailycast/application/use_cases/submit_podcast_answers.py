"""
Submit Podcast Answers Use Case.
"""
from dailycast.application.dtos.podcast_dtos import PodcastDetailDTO, SubmitAnswersCommand
from dailycast.application.ports.outbound.dailycast_repository_port import DailyCastRepositoryPort
from dailycast.domain.exceptions import DailycastError, DailyPodcastNotFoundError


class SubmitPodcastAnswersUseCase:
    """Use case to record a learner's answers to podcast questions."""

    def __init__(self, repository: DailyCastRepositoryPort):
        self.repository = repository

    def execute(self, request: SubmitAnswersCommand) -> PodcastDetailDTO:
        podcast = self.repository.get_by_id(request.podcast_id)
        if not podcast:
            raise DailyPodcastNotFoundError(request.podcast_id)

        # Permissions: only owner or staff can submit answers
        if podcast.user_id != request.user_id and not request.is_staff:
            raise DailycastError("Permission denied: You cannot submit answers for another user's podcast.")

        # Invariant validation: check for missing questions
        questions = podcast.questions_asked or []
        for q in questions:
            if q not in request.answers:
                raise DailycastError(f"Missing answer for question: '{q}'")

        # Update answers
        podcast.student_answers = request.answers
        saved = self.repository.save(podcast)

        user_stats = self.repository.get_user_stats(saved.user_id)
        username = user_stats.get("username", f"User {saved.user_id}")

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
