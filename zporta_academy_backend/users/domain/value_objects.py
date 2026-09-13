"""
Domain value objects for Users.
Pure Python, zero framework dependencies.
"""
from dataclasses import dataclass
from enum import Enum
import re
from core.shared_kernel.domain.value_objects import ValueObject


class UserRole(str, Enum):
    EXPLORER = "explorer"
    GUIDE = "guide"
    BOTH = "both"

    @classmethod
    def from_string(cls, role_str: str) -> "UserRole":
        clean = (role_str or "explorer").strip().lower()
        try:
            return cls(clean)
        except ValueError:
            return cls.EXPLORER


@dataclass(frozen=True)
class EmailAddress(ValueObject):
    """Validated and normalized email address value object."""
    value: str

    def __post_init__(self) -> None:
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Email cannot be empty")
        normalized = self.value.strip().lower()
        pattern = r"^[\w\.\+\-]+@[\w\.\-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, normalized):
            raise ValueError(f"Invalid email address format: {self.value}")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Username(ValueObject):
    """Validated and normalized username value object."""
    value: str

    def __post_init__(self) -> None:
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Username cannot be empty")
        normalized = self.value.strip()
        if len(normalized) < 3 or len(normalized) > 30:
            raise ValueError("Username must be between 3 and 30 characters")
        if not re.match(r"^[\w.@+-]+$", normalized):
            raise ValueError("Username contains invalid characters")
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
