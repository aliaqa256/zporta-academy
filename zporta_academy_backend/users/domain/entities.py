"""
Domain entities for Users and Profiles.
Pure Python, zero framework dependencies.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from core.shared_kernel.domain.base_entity import BaseEntity
from .value_objects import UserRole, EmailAddress, Username


@dataclass(eq=False)
class UserEntity(BaseEntity[int]):
    """Pure domain entity representing a User."""
    username: str = ""
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False

    @property
    def full_name(self) -> str:
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.username


@dataclass(eq=False)
class ProfileEntity(BaseEntity[int]):
    """Pure domain entity representing a User Profile."""
    user_id: int = 0
    display_name: str = ""
    role: str = "explorer"
    bio: str = ""
    active_guide: bool = False
    can_invite_teachers: bool = False
    growth_score: int = 0
    impact_score: int = 0
    teacher_tagline: Optional[str] = None
    teacher_about: Optional[str] = None
    teaching_specialties: Optional[str] = None

    @property
    def is_teacher(self) -> bool:
        return self.role in ("guide", "both") or self.active_guide


@dataclass
class UserPreferenceEntity:
    """Pure domain entity representing user preferences."""
    user_id: int
    interested_subjects: List[int] = field(default_factory=list)
    languages_spoken: List[str] = field(default_factory=list)
    location: Optional[str] = None
