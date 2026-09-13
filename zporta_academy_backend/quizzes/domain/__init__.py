"""
Domain layer for Quizzes.
Zero Django dependencies.
"""
from .entities import QuizEntity, QuestionEntity, QuizReportEntity, QuizShareEntity
from .value_objects import QuestionType, QuizType, QuizStatus, DifficultyLevel
from .policies import GradingPolicy, QuizAccessPolicy
from .exceptions import (
    QuizNotFoundError,
    QuestionNotFoundError,
    QuizAccessDeniedError,
    InvalidQuizAnswerError
)

__all__ = [
    "QuizEntity",
    "QuestionEntity",
    "QuizReportEntity",
    "QuizShareEntity",
    "QuestionType",
    "QuizType",
    "QuizStatus",
    "DifficultyLevel",
    "GradingPolicy",
    "QuizAccessPolicy",
    "QuizNotFoundError",
    "QuestionNotFoundError",
    "QuizAccessDeniedError",
    "InvalidQuizAnswerError",
]
