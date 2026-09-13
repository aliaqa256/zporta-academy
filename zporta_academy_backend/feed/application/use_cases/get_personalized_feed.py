from typing import Optional
from feed.domain.policies import FeedRankingPolicy
from ..dtos import FeedQuizItemDTO, PersonalizedFeedDTO
from ..ports.outbound.feed_repository_port import FeedRepositoryPort


class GetPersonalizedFeedUseCase:
    """Orchestrates generation of the composite personalized feed."""

    def __init__(self, repository: FeedRepositoryPort):
        self.repository = repository

    def execute(self, user_id: int, limit_per_section: int = 10) -> PersonalizedFeedDTO:
        explore_entities = self.repository.get_explore_quizzes(user_id, limit=limit_per_section)
        personalized_entities = self.repository.get_personalized_quizzes(user_id, limit=limit_per_section)
        review_entities = self.repository.get_review_quizzes(user_id, limit=limit_per_section)

        def to_dto(item):
            return FeedQuizItemDTO(
                id=item.id,
                title=item.title,
                permalink=item.permalink,
                difficulty_score=item.difficulty_score,
                difficulty_level=item.difficulty_level,
                subject_title=item.subject_title,
                match_score=item.match_score,
                question_count=item.question_count,
                estimated_time_min=item.estimated_time_min,
                is_review=item.is_review,
                due_date=item.due_date
            )

        return PersonalizedFeedDTO(
            user_id=user_id,
            explore_quizzes=[to_dto(x) for x in explore_entities],
            personalized_quizzes=[to_dto(x) for x in personalized_entities],
            review_quizzes=[to_dto(x) for x in review_entities]
        )
