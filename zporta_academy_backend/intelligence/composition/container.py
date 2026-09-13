"""
Composition Root for Intelligence Domain.
Constructs use cases with concrete adapters.
"""
from intelligence.adapters.outbound.persistence.django_intelligence_repository import (
    DjangoAbilityRepository,
    DjangoDifficultyRepository,
    DjangoMatchScoreRepository
)
from intelligence.application.use_cases.get_user_ability_overview import GetUserAbilityOverviewUseCase
from intelligence.application.use_cases.calculate_elo_update import CalculateEloUpdateUseCase


def build_ability_repository() -> DjangoAbilityRepository:
    return DjangoAbilityRepository()


def build_difficulty_repository() -> DjangoDifficultyRepository:
    return DjangoDifficultyRepository()


def build_match_score_repository() -> DjangoMatchScoreRepository:
    return DjangoMatchScoreRepository()


def build_get_user_ability_overview_use_case() -> GetUserAbilityOverviewUseCase:
    return GetUserAbilityOverviewUseCase(
        ability_repo=build_ability_repository()
    )


def build_calculate_elo_update_use_case() -> CalculateEloUpdateUseCase:
    return CalculateEloUpdateUseCase(
        ability_repo=build_ability_repository(),
        difficulty_repo=build_difficulty_repository()
    )
