"""
Domain value objects for Courses.
Pure Python, zero framework dependencies.
"""
from dataclasses import dataclass
from enum import Enum
from core.shared_kernel.domain.value_objects import ValueObject


class CourseType(str, Enum):
    FREE = "free"
    PREMIUM = "premium"


@dataclass(frozen=True)
class CoursePrice(ValueObject):
    """Course price value object."""
    amount: float

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Course price cannot be negative")
        object.__setattr__(self, "amount", round(float(self.amount), 2))

    @property
    def is_free(self) -> bool:
        return self.amount == 0.0
