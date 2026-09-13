"""
Application Layer DTOs for Intelligence.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass(frozen=True)
class LearnerAbilityDTO:
    user_id: int
    username: str
    overall_ability_score: Optional[float]
    ability_level: str
    total_quizzes_attempted: int
    total_correct_answers: int
    recent_performance_trend: float
    global_rank: Optional[int]
    percentile: Optional[float]
    ability_by_subject: Dict[str, float] = field(default_factory=dict)
    message: Optional[str] = None


@dataclass(frozen=True)
class LearningPathItemDTO:
    quiz_id: int
    title: str
    subject: Optional[str]
    difficulty_score: float
    difficulty_level: str
    match_score: float
    why: str
    estimated_time_minutes: int
    permalink: str


@dataclass(frozen=True)
class LearningPathResultDTO:
    path: List[LearningPathItemDTO]
    total_items: int
    message: Optional[str] = None


@dataclass(frozen=True)
class EloUpdateCommand:
    user_id: int
    content_id: int
    content_type: str  # 'quiz' or 'question'
    is_correct: bool


@dataclass(frozen=True)
class EloUpdateResultDTO:
    previous_ability: float
    new_ability: float
    difficulty_score: float
    delta: float
