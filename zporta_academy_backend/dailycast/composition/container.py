"""
DailyCast Composition Container.
"""
from dailycast.adapters.outbound.audio.pydub_audio_stitcher import PydubAudioStitcherAdapter
from dailycast.adapters.outbound.persistence.django_dailycast_repository import DjangoDailyCastRepository
from dailycast.adapters.outbound.tts.polly_tts_adapter import PollyTTSAdapter
from dailycast.application.ports.outbound.dailycast_repository_port import DailyCastRepositoryPort
from dailycast.application.ports.outbound.podcast_stitcher_port import PodcastStitcherPort
from dailycast.application.ports.outbound.podcast_tts_port import PodcastTTSPort
from dailycast.application.use_cases.create_podcast import CreatePodcastUseCase
from dailycast.application.use_cases.evaluate_podcast_accuracy import EvaluatePodcastAccuracyUseCase
from dailycast.application.use_cases.get_podcast_detail import GetPodcastDetailUseCase
from dailycast.application.use_cases.get_student_progress import GetStudentProgressUseCase
from dailycast.application.use_cases.submit_podcast_answers import SubmitPodcastAnswersUseCase


def build_dailycast_repository() -> DailyCastRepositoryPort:
    return DjangoDailyCastRepository()


def build_podcast_tts_adapter() -> PodcastTTSPort:
    return PollyTTSAdapter()


def build_audio_stitcher_adapter() -> PodcastStitcherPort:
    return PydubAudioStitcherAdapter()


def build_create_podcast_use_case(
    repository: DailyCastRepositoryPort = None,
    tts_provider: PodcastTTSPort = None,
    enforce_cooldown: bool = False,
) -> CreatePodcastUseCase:
    return CreatePodcastUseCase(
        repository=repository or build_dailycast_repository(),
        tts_provider=tts_provider or build_podcast_tts_adapter(),
        enforce_cooldown=enforce_cooldown,
    )


def build_get_podcast_detail_use_case(
    repository: DailyCastRepositoryPort = None,
) -> GetPodcastDetailUseCase:
    return GetPodcastDetailUseCase(
        repository=repository or build_dailycast_repository()
    )


def build_evaluate_podcast_accuracy_use_case(
    repository: DailyCastRepositoryPort = None,
) -> EvaluatePodcastAccuracyUseCase:
    return EvaluatePodcastAccuracyUseCase(
        repository=repository or build_dailycast_repository()
    )


def build_submit_podcast_answers_use_case(
    repository: DailyCastRepositoryPort = None,
) -> SubmitPodcastAnswersUseCase:
    return SubmitPodcastAnswersUseCase(
        repository=repository or build_dailycast_repository()
    )


def build_get_student_progress_use_case(
    repository: DailyCastRepositoryPort = None,
) -> GetStudentProgressUseCase:
    return GetStudentProgressUseCase(
        repository=repository or build_dailycast_repository()
    )
