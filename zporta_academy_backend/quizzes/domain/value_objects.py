"""
Value objects and Enums for Quizzes domain.
Pure Python.
"""
from enum import Enum


class QuestionType(str, Enum):
    MCQ = "mcq"
    MULTI = "multi"
    SHORT = "short"
    DRAGDROP = "dragdrop"
    SORT = "sort"


class QuizType(str, Enum):
    FREE = "free"
    PREMIUM = "premium"


class QuizStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
