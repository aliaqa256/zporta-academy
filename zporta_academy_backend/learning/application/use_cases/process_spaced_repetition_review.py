"""
Process Spaced Repetition Review Use Case.
"""
from datetime import datetime, timezone
from learning.application.dtos.study_dtos import ReviewCardCommand, ReviewResultDTO
from learning.application.ports.outbound.learning_repository_port import LearningRepositoryPort
from learning.domain.entities import StudyItemEntity
from learning.domain.exceptions import InvalidReviewRatingError, StudyCardNotFoundError
from learning.domain.policies import SpacedRepetitionPolicy
from learning.domain.value_objects import ReviewRating


class ProcessSpacedRepetitionReviewUseCase:
    """Use case to grade a card review and schedule the next spaced repetition interval."""

    def __init__(self, repository: LearningRepositoryPort):
        self._repository = repository

    def execute(self, cmd: ReviewCardCommand) -> ReviewResultDTO:
        if cmd.rating not in ReviewRating._value2member_map_:
            raise InvalidReviewRatingError(f"Invalid rating: '{cmd.rating}'. Valid options: again, hard, good, easy.")

        rating_enum = ReviewRating(cmd.rating)

        item = self._repository.get_study_item(cmd.item_id)
        if not item:
            # Create a new study item entity if not previously scheduled
            item = StudyItemEntity(
                id=cmd.item_id,
                user_id=cmd.user_id,
                title=f"Study Item {cmd.item_id}",
            )

        now = datetime.now(timezone.utc)
        reps, ease, interval, due = SpacedRepetitionPolicy.calculate_next_schedule(
            repetitions=item.repetitions,
            ease_factor=item.ease_factor,
            interval_days=item.interval_days,
            rating=rating_enum,
            now=now,
        )

        item.repetitions = reps
        item.ease_factor = ease
        item.interval_days = interval
        item.next_review_at = due
        item.last_reviewed_at = now

        saved = self._repository.save_study_item(item)

        return ReviewResultDTO(
            item_id=saved.id or cmd.item_id,
            user_id=saved.user_id,
            repetitions=saved.repetitions,
            ease_factor=saved.ease_factor,
            interval_days=saved.interval_days,
            next_review_at=saved.next_review_at or due,
        )
