"""
Evaluate Podcast Accuracy Use Case.
"""
from dailycast.application.dtos.podcast_dtos import AccuracyCheckResultDTO
from dailycast.application.ports.outbound.dailycast_repository_port import DailyCastRepositoryPort
from dailycast.domain.exceptions import DailyPodcastNotFoundError
from dailycast.domain.policies import PodcastAccuracyPolicy


class EvaluatePodcastAccuracyUseCase:
    """Use case to validate podcast accuracy against enrolled courses, audio existence, and timing."""

    def __init__(self, repository: DailyCastRepositoryPort):
        self.repository = repository

    def execute(self, podcast_id: int) -> AccuracyCheckResultDTO:
        podcast = self.repository.get_by_id(podcast_id)
        if not podcast:
            raise DailyPodcastNotFoundError(podcast_id)

        user_stats = self.repository.get_user_stats(podcast.user_id)
        username = user_stats.get("username", f"User {podcast.user_id}")

        report = PodcastAccuracyPolicy.evaluate_accuracy(podcast)

        metadata = {
            "podcast_id": podcast.id,
            "user": username,
            "primary_language": podcast.primary_language,
            "secondary_language": podcast.secondary_language or "None",
            "output_format": podcast.output_format.value,
            "llm_provider": podcast.llm_provider,
            "tts_provider": podcast.tts_provider,
        }

        return AccuracyCheckResultDTO(
            status=report.get("status", "success"),
            accuracy_score=report.get("accuracy_score", 1.0),
            issues=report.get("issues", []),
            warnings=report.get("warnings", []),
            metadata=metadata,
            content_checks=report.get("content_checks", {}),
            recommendation=report.get("recommendation", "✅ Ready for use"),
        )
