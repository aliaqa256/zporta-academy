from typing import List, Optional
from django.contrib.auth import get_user_model
from feed.domain.entities import FeedQuizItemEntity
from feed.application.ports.outbound.feed_repository_port import FeedRepositoryPort
from feed.services import get_explore_quizzes, get_personalized_quizzes, get_review_queue

User = get_user_model()


class DjangoFeedRepository(FeedRepositoryPort):
    """Django ORM adapter for feed repository."""

    def get_explore_quizzes(self, user_id: int, limit: int = 10) -> List[FeedQuizItemEntity]:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return []
        data = get_explore_quizzes(user, limit)
        return self._to_entities(data)

    def get_personalized_quizzes(self, user_id: int, limit: int = 10) -> List[FeedQuizItemEntity]:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return []
        data = get_personalized_quizzes(user, limit)
        return self._to_entities(data)

    def get_review_quizzes(self, user_id: int, limit: int = 10) -> List[FeedQuizItemEntity]:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return []
        data = get_review_queue(user, limit)
        return self._to_entities(data)

    def _to_entities(self, data_list: list) -> List[FeedQuizItemEntity]:
        entities = []
        for item in data_list:
            if isinstance(item, dict):
                entities.append(
                    FeedQuizItemEntity(
                        id=item.get("id", 0),
                        title=item.get("title", ""),
                        permalink=item.get("permalink", ""),
                        difficulty_score=float(item.get("difficulty_score", 500.0) or 500.0),
                        difficulty_level=item.get("difficulty_level", "Medium"),
                        subject_title=item.get("subject_title", ""),
                        match_score=float(item.get("match_score", 0.0) or 0.0),
                        question_count=item.get("question_count", 0),
                        estimated_time_min=item.get("estimated_time_min", 5),
                        is_review=bool(item.get("is_review", False)),
                        due_date=item.get("due_date")
                    )
                )
        return entities
