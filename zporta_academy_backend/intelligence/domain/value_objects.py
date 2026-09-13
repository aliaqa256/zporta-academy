"""
Value Objects and Enums for Intelligence domain.
Pure Python.
"""
from dataclasses import dataclass
from enum import Enum


class AbilityLevel(str, Enum):
    UNRANKED = "Unranked"
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class DifficultyTier(str, Enum):
    BEGINNER = "beginner"
    BEGINNER_MEDIUM = "beginner_medium"
    MEDIUM = "medium"
    MEDIUM_HARD = "medium_hard"
    HARD = "hard"


@dataclass(frozen=True)
class EloScore:
    value: float

    def __post_init__(self):
        if not (0.0 <= self.value <= 1000.0):
            # Clamp to 0..1000 range
            object.__setattr__(self, 'value', max(0.0, min(1000.0, float(self.value))))

    @property
    def int_value(self) -> int:
        return int(round(self.value))
