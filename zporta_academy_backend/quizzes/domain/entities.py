"""
Pure domain entities for Quizzes and Questions.
Zero Django dependencies.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from core.shared_kernel.domain.base_entity import BaseEntity
from .value_objects import QuestionType, QuizType, QuizStatus, DifficultyLevel


@dataclass(eq=False)
class QuestionEntity(BaseEntity[int]):
    quiz_id: int = 0
    question_type: QuestionType = QuestionType.MCQ
    permalink: str = ""
    question_text: str = ""
    question_image: Optional[str] = None
    question_image_alt: str = ""
    question_audio: Optional[str] = None
    option1: Optional[str] = None
    option2: Optional[str] = None
    option3: Optional[str] = None
    option4: Optional[str] = None
    correct_option: Optional[int] = None
    correct_options: Optional[List[Any]] = None
    correct_answer: Optional[str] = None
    question_data: Optional[Dict[str, Any]] = None
    hint1: str = ""
    hint2: str = ""
    computed_difficulty_score: Optional[float] = None
    avg_time_spent_ms: Optional[int] = None
    success_rate: Optional[float] = None


@dataclass(eq=False)
class QuizEntity(BaseEntity[int]):
    title: str = ""
    content: str = ""
    is_locked: bool = False
    lesson_id: Optional[int] = None
    subject_id: Optional[int] = None
    course_id: Optional[int] = None
    created_by_id: int = 0
    created_at: Optional[datetime] = None
    quiz_type: QuizType = QuizType.FREE
    permalink: str = ""
    status: QuizStatus = QuizStatus.DRAFT
    published_at: Optional[datetime] = None
    difficulty_level: DifficultyLevel = DifficultyLevel.MEDIUM
    computed_difficulty_score: Optional[float] = None
    attempt_count: int = 0
    questions: List[QuestionEntity] = field(default_factory=list)

    @property
    def is_published(self) -> bool:
        return self.status == QuizStatus.PUBLISHED or self.status == "published"


@dataclass(eq=False)
class QuizReportEntity(BaseEntity[int]):
    quiz_id: int = 0
    reporter_id: int = 0
    message: str = ""
    suggested_correction: str = ""
    created_at: Optional[datetime] = None
    is_resolved: bool = False


@dataclass(eq=False)
class QuizShareEntity(BaseEntity[int]):
    quiz_id: int = 0
    from_user_id: int = 0
    to_user_id: int = 0
    message: str = ""
    created_at: Optional[datetime] = None
