from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class FeedQuizItemEntity:
    id: int
    title: str
    permalink: str
    difficulty_score: float = 500.0
    difficulty_level: str = "Medium"
    subject_title: str = ""
    match_score: float = 0.0
    question_count: int = 0
    estimated_time_min: int = 5
    is_review: bool = False
    due_date: Optional[str] = None


@dataclass
class PersonalizedFeedEntity:
    user_id: int
    explore_quizzes: List[FeedQuizItemEntity] = field(default_factory=list)
    personalized_quizzes: List[FeedQuizItemEntity] = field(default_factory=list)
    review_quizzes: List[FeedQuizItemEntity] = field(default_factory=list)
