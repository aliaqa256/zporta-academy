"""
Use Case: Get User Ability Profile Overview.
"""
from core.shared_kernel.domain.result import Result, ok, err
from intelligence.domain.policies import DifficultyClassificationPolicy
from intelligence.application.dtos import LearnerAbilityDTO
from intelligence.application.ports.outbound.ability_repository_port import AbilityRepositoryPort


class GetUserAbilityOverviewUseCase:
    def __init__(self, ability_repo: AbilityRepositoryPort):
        self._ability_repo = ability_repo

    def execute(self, user_id: int, username: str = "") -> Result[LearnerAbilityDTO, Exception]:
        profile = self._ability_repo.get_by_user_id(user_id)
        if not profile:
            # Return unranked DTO for new users
            dto = LearnerAbilityDTO(
                user_id=user_id,
                username=username,
                overall_ability_score=None,
                ability_level="Unranked",
                total_quizzes_attempted=0,
                total_correct_answers=0,
                recent_performance_trend=0.0,
                global_rank=None,
                percentile=None,
                ability_by_subject={},
                message="Your ability profile is being computed. Please attempt some quizzes first!"
            )
            return ok(dto)

        level_str = DifficultyClassificationPolicy.classify_ability_level(
            profile.overall_ability_score,
            total_attempts=profile.total_quizzes_attempted
        )

        dto = LearnerAbilityDTO(
            user_id=profile.user_id,
            username=profile.username or username,
            overall_ability_score=profile.overall_ability_score,
            ability_level=level_str,
            total_quizzes_attempted=profile.total_quizzes_attempted,
            total_correct_answers=profile.total_correct_answers,
            recent_performance_trend=profile.recent_performance_trend,
            global_rank=profile.global_rank,
            percentile=profile.percentile,
            ability_by_subject=profile.ability_by_subject
        )
        return ok(dto)
