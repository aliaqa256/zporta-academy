"""
Learning & Spaced Repetition Domain Value Objects.
"""
from enum import Enum


class ReviewRating(str, Enum):
    AGAIN = "again"   # Complete blackout / reset interval
    HARD = "hard"     # Recalled with heavy effort
    GOOD = "good"     # Normal recall
    EASY = "easy"     # Instant recall


class NotePrivacy(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    MENTION = "mention"


class StudyEventType(str, Enum):
    LESSON_CLICKED = "lesson_clicked"
    LESSON_COMPLETED = "lesson_completed"
    QUIZ_STARTED = "quiz_started"
    QUIZ_SUBMITTED = "quiz_submitted"
    QUIZ_ANSWER_SUBMITTED = "quiz_answer_submitted"
