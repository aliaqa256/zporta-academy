from gamification.application.ports.outbound.gamification_repository_port import GamificationRepositoryPort
from gamification.application.use_cases.record_activity import RecordActivityUseCase
from gamification.adapters.outbound.persistence.django_gamification_repository import DjangoGamificationRepository


def build_gamification_repository() -> GamificationRepositoryPort:
    return DjangoGamificationRepository()


def build_record_activity_use_case(
    repository: GamificationRepositoryPort = None
) -> RecordActivityUseCase:
    return RecordActivityUseCase(
        repository=repository or build_gamification_repository()
    )
