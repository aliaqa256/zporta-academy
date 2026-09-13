"""
Pure domain entities for User Ability, Content Difficulty, and Match Scores.
Zero Django dependencies.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from core.shared_kernel.domain.base_entity import BaseEntity
from .value_objects import EloScore, AbilityLevel, DifficultyTier


@dataclass(eq=False)
class UserAbilityEntity(BaseEntity[int]):
    id: Optional[int] = None
    user_id: int = 0
    username: str = ""
    overall_ability_score: float = 400.0
    ability_by_subject: Dict[str, float] = field(default_factory=dict)
    ability_by_tag: Dict[str, float] = field(default_factory=dict)
    total_quizzes_attempted: int = 0
    total_correct_answers: int = 0
    recent_performance_trend: float = 0.0
    global_rank: Optional[int] = None
    percentile: Optional[float] = None
    last_computed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def ability_level(self) -> AbilityLevel:
        if self.total_quizzes_attempted == 0:
            return AbilityLevel.UNRANKED
        score = self.overall_ability_score
        if score < 300:
            return AbilityLevel.BEGINNER
        elif score < 500:
            return AbilityLevel.INTERMEDIATE
        elif score < 700:
            return AbilityLevel.ADVANCED
        else:
            return AbilityLevel.EXPERT

    def get_subject_ability(self, subject_id: int) -> float:
        return self.ability_by_subject.get(str(subject_id), self.overall_ability_score)


@dataclass(eq=False)
class ContentDifficultyEntity(BaseEntity[int]):
    id: Optional[int] = None
    content_type: str = "quiz"
    object_id: int = 0
    computed_difficulty_score: float = 400.0
    avg_time_spent_seconds: Optional[float] = None
    success_rate: float = 0.0
    attempt_count: int = 0
    difficulty_by_user_segment: Dict[str, float] = field(default_factory=dict)
    last_computed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def difficulty_tier(self) -> DifficultyTier:
        score = self.computed_difficulty_score
        if score < 320:
            return DifficultyTier.BEGINNER
        elif score < 420:
            return DifficultyTier.BEGINNER_MEDIUM
        elif score < 520:
            return DifficultyTier.MEDIUM
        elif score < 620:
            return DifficultyTier.MEDIUM_HARD
        else:
            return DifficultyTier.HARD


@dataclass(eq=False)
class MatchScoreEntity(BaseEntity[int]):
    id: Optional[int] = None
    user_id: int = 0
    content_type: str = "quiz"
    object_id: int = 0
    match_score: float = 50.0
    difficulty_gap: float = 0.0
    zpd_score: Optional[float] = None
    preference_alignment_score: Optional[float] = None
    topic_similarity_score: Optional[float] = None
    recency_penalty: float = 0.0
    computed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
