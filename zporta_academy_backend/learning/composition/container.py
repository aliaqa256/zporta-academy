"""
Learning Composition Container.
"""
from learning.adapters.outbound.persistence.django_learning_repository import DjangoLearningRepository
from learning.application.ports.outbound.learning_repository_port import LearningRepositoryPort
from learning.application.use_cases.get_study_dashboard import GetStudyDashboardUseCase
from learning.application.use_cases.process_spaced_repetition_review import ProcessSpacedRepetitionReviewUseCase


def build_learning_repository() -> LearningRepositoryPort:
    return DjangoLearningRepository()


def build_get_study_dashboard_use_case(
    repository: LearningRepositoryPort = None,
) -> GetStudyDashboardUseCase:
    return GetStudyDashboardUseCase(
        repository=repository or build_learning_repository()
    )


def build_process_spaced_repetition_review_use_case(
    repository: LearningRepositoryPort = None,
) -> ProcessSpacedRepetitionReviewUseCase:
    return ProcessSpacedRepetitionReviewUseCase(
        repository=repository or build_learning_repository()
    )
