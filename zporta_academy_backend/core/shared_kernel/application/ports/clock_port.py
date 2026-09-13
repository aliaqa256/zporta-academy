"""
Clock Port interface for deterministic time operations across use cases.
"""
from abc import ABC, abstractmethod
from datetime import datetime


class ClockPort(ABC):
    """Abstract port for time retrieval."""
    @abstractmethod
    def now(self) -> datetime:
        """Returns the current timestamp in UTC."""
        ...
