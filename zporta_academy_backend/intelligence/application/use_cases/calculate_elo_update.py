"""
Use Case: Calculate ELO Update on Quiz/Question attempt.
"""
from core.shared_kernel.domain.result import Result, ok, err
from intelligence.domain.policies import EloCalculationPolicy
from intelligence.domain.entities import UserAbilityEntity
from intelligence.application.dtos import EloUpdateCommand, EloUpdateResultDTO
from intelligence.application.ports.outbound.ability_repository_port import AbilityRepositoryPort
from intelligence.application.ports.outbound.difficulty_repository_port import DifficultyRepositoryPort


class CalculateEloUpdateUseCase:
    def __init__(
        self,
        ability_repo: AbilityRepositoryPort,
        difficulty_repo: DifficultyRepositoryPort
    ):
        self._ability_repo = ability_repo
        self._difficulty_repo = difficulty_repo

    def execute(self, cmd: EloUpdateCommand) -> Result[EloUpdateResultDTO, Exception]:
        ability = self._ability_repo.get_by_user_id(cmd.user_id)
        current_ability = ability.overall_ability_score if ability else 400.0
        attempts = ability.total_quizzes_attempted if ability else 0

        diff_profile = self._difficulty_repo.get_by_content(cmd.content_type, cmd.content_id)
        diff_score = diff_profile.computed_difficulty_score if diff_profile else 400.0

        actual_score = 1.0 if cmd.is_correct else 0.0
        new_ability = EloCalculationPolicy.update_rating(
            current_rating=current_ability,
            content_difficulty=diff_score,
            actual_score=actual_score,
            attempts_count=attempts
        )

        if ability:
            ability.overall_ability_score = new_ability
            ability.total_quizzes_attempted += 1
            if cmd.is_correct:
                ability.total_correct_answers += 1
            self._ability_repo.save(ability)

        result = EloUpdateResultDTO(
            previous_ability=current_ability,
            new_ability=new_ability,
            difficulty_score=diff_score,
            delta=round(new_ability - current_ability, 2)
        )
        return ok(result)
