"""
Outbound Port interface for logging quiz answers and updating spaced repetition stats.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class QuizAnswerLogPort(ABC):
    """Abstract port for logging attempts and updating spaced-repetition memory stats."""

    @abstractmethod
    def log_answer_event(
        self,
        user_id: int,
        quiz_id: int,
        question_id: int,
        metadata: Dict[str, Any]
    ) -> None:
        ...

    @abstractmethod
    def update_question_memory_stat(
        self,
        user_id: int,
        question_id: int,
        quality_of_recall: int,
        time_spent_ms: Optional[int]
    ) -> Optional[str]:
        """Returns next_review_at as ISO string if available."""
        ...
