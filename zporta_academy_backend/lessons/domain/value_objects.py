"""
Domain value objects for Lessons.
Pure Python, zero framework dependencies.
"""
from dataclasses import dataclass
from enum import Enum
from core.shared_kernel.domain.value_objects import ValueObject


class LessonStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class ContentAccessLevel(str, Enum):
    FULL = "full"
    PREVIEW = "preview"
    LOCKED = "locked"
