"""
Application Layer DTOs for Quizzes.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass(frozen=True)
class QuestionDTO:
    id: int
    quiz_id: int
    question_type: str
    permalink: str
    question_text: str
    question_image: Optional[str]
    question_image_alt: str
    question_audio: Optional[str]
    option1: Optional[str]
    option2: Optional[str]
    option3: Optional[str]
    option4: Optional[str]
    correct_option: Optional[int]
    correct_options: Optional[List[Any]]
    correct_answer: Optional[str]
    question_data: Optional[Dict[str, Any]]
    hint1: str
    hint2: str
    computed_difficulty_score: Optional[float]
    stats: Optional[Dict[str, int]] = None


@dataclass(frozen=True)
class QuizSummaryDTO:
    id: int
    title: str
    permalink: str
    quiz_type: str
    status: str
    created_by_id: int
    created_by_name: str
    subject_id: Optional[int]
    subject_name: Optional[str]
    course_id: Optional[int]
    course_title: Optional[str]
    attempt_count: int
    difficulty_level: Optional[str]
    computed_difficulty_score: Optional[float]


@dataclass(frozen=True)
class QuizDetailDTO:
    id: int
    title: str
    content: str
    permalink: str
    quiz_type: str
    status: str
    created_by_id: int
    created_by_name: str
    subject_id: Optional[int]
    subject_name: Optional[str]
    course_id: Optional[int]
    course_title: Optional[str]
    is_locked: bool
    difficulty_level: Optional[str]
    computed_difficulty_score: Optional[float]
    questions: List[QuestionDTO] = field(default_factory=list)


@dataclass(frozen=True)
class RecordAnswerCommand:
    quiz_id: int
    question_id: int
    user_id: int
    selected_option: Optional[Any] = None
    selected_answer_text: Optional[str] = None
    selected_option_key: Optional[str] = None
    selected_options: Optional[List[Any]] = None
    time_spent_ms: Optional[int] = None
    hints_used: Optional[List[int]] = None


@dataclass(frozen=True)
class AnswerEvaluationResultDTO:
    is_correct: bool
    message: str
    quality_of_recall: int
    next_review_at: Optional[str] = None
    processed_answer: Optional[Any] = None
    correct_expected: Optional[Any] = None


@dataclass(frozen=True)
class QuestionNavigationDTO:
    prev_permalink: Optional[str]
    prev_number: Optional[int]
    next_permalink: Optional[str]
    next_number: Optional[int]


@dataclass(frozen=True)
class QuestionDetailDTO:
    question: QuestionDTO
    quiz_id: int
    quiz_title: str
    quiz_permalink: str
    total_questions: int
    current_position: int
    navigation: QuestionNavigationDTO
