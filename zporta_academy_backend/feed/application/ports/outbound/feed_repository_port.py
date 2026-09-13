from abc import ABC, abstractmethod
from typing import List, Optional
from feed.domain.entities import FeedQuizItemEntity


class FeedRepositoryPort(ABC):
    """Abstract port for quiz feed retrieval."""

    @abstractmethod
    def get_explore_quizzes(self, user_id: int, limit: int = 10) -> List[FeedQuizItemEntity]:
        pass

    @abstractmethod
    def get_personalized_quizzes(self, user_id: int, limit: int = 10) -> List[FeedQuizItemEntity]:
        pass

    @abstractmethod
    def get_review_quizzes(self, user_id: int, limit: int = 10) -> List[FeedQuizItemEntity]:
        pass
