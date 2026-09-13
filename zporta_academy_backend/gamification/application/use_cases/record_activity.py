from typing import Optional
from gamification.domain.policies import GamificationPointsPolicy
from ..dtos import ActivityLogCommand, UserScoreDTO
from ..ports.outbound.gamification_repository_port import GamificationRepositoryPort


class RecordActivityUseCase:
    """Awards points and logs activity events."""

    def __init__(self, repository: GamificationRepositoryPort):
        self.repository = repository

    def execute(self, cmd: ActivityLogCommand) -> Optional[UserScoreDTO]:
        points = GamificationPointsPolicy.get_points_for_activity(cmd.activity_type)

        activity = self.repository.log_activity(
            user_id=cmd.user_id,
            activity_type=cmd.activity_type,
            points=points,
            unique_key=cmd.unique_key,
            is_mistake=cmd.is_mistake,
            metadata=cmd.metadata,
            time_spent_seconds=cmd.time_spent_seconds
        )

        if activity:
            # Recalculate or update score
            score = self.repository.recalculate_user_score(cmd.user_id)
            return UserScoreDTO(
                user_id=score.user_id,
                total_points=score.total_points,
                lessons_completed=score.lessons_completed,
                courses_completed=score.courses_completed,
                correct_answers=score.correct_answers,
                last_calculated=score.last_calculated
            )
        return None
