"""
Application Layer DTOs for Users and Authentication.
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass(frozen=True)
class RegisterUserCommand:
    username: str
    email: str
    password: str
    role: str = "explorer"
    bio: str = ""


@dataclass(frozen=True)
class AuthenticateUserCommand:
    credential: str  # username or email
    password: str


@dataclass(frozen=True)
class AuthResultDTO:
    token: str
    user_id: int
    username: str
    email: str
    role: str
    active_guide: bool
    locale: str = "en"
    preferences: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class UserProfileDTO:
    user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    display_name: str
    role: str
    bio: str
    active_guide: bool
    is_staff: bool
    date_joined: str
    growth_score: int
    impact_score: int
    profile_image_url: Optional[str] = None
    teacher_tagline: Optional[str] = None
    teacher_about: Optional[str] = None
    teaching_specialties: Optional[str] = None


@dataclass(frozen=True)
class UpdateProfileCommand:
    user_id: int
    display_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    role: Optional[str] = None
    teacher_tagline: Optional[str] = None
    teacher_about: Optional[str] = None
    teaching_specialties: Optional[str] = None
