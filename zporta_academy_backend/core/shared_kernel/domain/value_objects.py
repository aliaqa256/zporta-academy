"""
Base Value Object abstractions and ubiquitous domain value types.
Value objects are immutable and compared by structural equality.
"""
from dataclasses import dataclass
from typing import Any
import re


@dataclass(frozen=True)
class ValueObject:
    """Base class for domain value objects."""
    pass


@dataclass(frozen=True)
class Slug(ValueObject):
    """Normalized URL slug value object."""
    value: str

    def __post_init__(self) -> None:
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Slug must be a non-empty string")
        raw = self.value.strip().lower()
        parts = [part.strip() for part in raw.split("/") if part.strip()]
        cleaned_parts = []
        for p in parts:
            cleaned = re.sub(r"[^a-zA-Z0-9-_]", "-", p)
            cleaned = re.sub(r"-+", "-", cleaned).strip("-")
            if cleaned:
                cleaned_parts.append(cleaned)
        final_slug = "/".join(cleaned_parts)
        if not final_slug:
            raise ValueError("Slug cannot be empty after normalization")
        object.__setattr__(self, "value", final_slug)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Money(ValueObject):
    """Monetary amount representation with currency."""
    amount_cents: int
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount_cents < 0:
            raise ValueError("Money amount cannot be negative")
        if not self.currency or len(self.currency) != 3:
            raise ValueError("Currency must be a 3-letter ISO code")
        object.__setattr__(self, "currency", self.currency.upper())

    @property
    def amount(self) -> float:
        return self.amount_cents / 100.0

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add different currencies: {self.currency} and {other.currency}")
        return Money(amount_cents=self.amount_cents + other.amount_cents, currency=self.currency)
