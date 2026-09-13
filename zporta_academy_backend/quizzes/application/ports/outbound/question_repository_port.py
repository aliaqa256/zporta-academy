"""
Outbound Port interface for Question persistence and navigation.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from quizzes.domain.entities import QuestionEntity


class QuestionRepositoryPort(ABC):
    """Abstract port for Question database access."""

    @abstractmethod
    def get_by_id(self, question_id: int, quiz_id: Optional[int] = None) -> Optional[QuestionEntity]:
        ...

    @abstractmethod
    def get_by_permalink(self, permalink: str) -> Optional[QuestionEntity]:
        ...

    @abstractmethod
    def list_by_quiz_id(self, quiz_id: int) -> List[QuestionEntity]:
        ...

    @abstractmethod
    def get_navigation_for_question(self, question_id: int, quiz_id: int) -> Tuple[Optional[QuestionEntity], Optional[QuestionEntity], int, int]:
        """Returns (prev_question, next_question, current_1_based_index, total_questions)."""
        ...
