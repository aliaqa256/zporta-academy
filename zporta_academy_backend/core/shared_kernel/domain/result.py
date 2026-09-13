"""
Result/Either pattern for railway-oriented error handling across domain and application layers.
Pure Python, zero framework dependencies.
"""
from typing import Generic, TypeVar, Union, Callable, Any, Optional
from dataclasses import dataclass

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")


@dataclass(frozen=True)
class Success(Generic[T]):
    """Represents a successful operation containing a value."""
    value: T

    @property
    def is_success(self) -> bool:
        return True

    @property
    def is_failure(self) -> bool:
        return False

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, default: Any) -> T:
        return self.value

    def unwrap_error(self) -> None:
        raise ValueError("Cannot unwrap error from a Success result")

    def map(self, fn: Callable[[T], U]) -> "Result[U, Any]":
        return Success(fn(self.value))

    def flat_map(self, fn: Callable[[T], "Result[U, Any]"]) -> "Result[U, Any]":
        return fn(self.value)


@dataclass(frozen=True)
class Failure(Generic[E]):
    """Represents a failed operation containing an error."""
    error: E

    @property
    def is_success(self) -> bool:
        return False

    @property
    def is_failure(self) -> bool:
        return True

    def unwrap(self) -> Any:
        if isinstance(self.error, Exception):
            raise self.error
        raise ValueError(f"Result failed with error: {self.error}")

    def unwrap_or(self, default: U) -> U:
        return default

    def unwrap_error(self) -> E:
        return self.error

    def map(self, fn: Callable[[Any], Any]) -> "Result[Any, E]":
        return self

    def flat_map(self, fn: Callable[[Any], Any]) -> "Result[Any, E]":
        return self


Result = Union[Success[T], Failure[E]]


def ok(value: T) -> Success[T]:
    """Convenience helper to create a Success result."""
    return Success(value)


def err(error: E) -> Failure[E]:
    """Convenience helper to create a Failure result."""
    return Failure(error)
