"""
Enrollment Domain Value Objects.
"""
from enum import Enum


class EnrollmentStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


class EnrollmentType(str, Enum):
    COURSE = "course"
    QUIZ = "quiz"
    LESSON = "lesson"
