"""
ClockPort adapter implementations (SystemClock for production, FrozenClock for deterministic testing).
"""
from datetime import datetime, timezone
from ..application.ports.clock_port import ClockPort


class SystemClock(ClockPort):
    """Production clock returning current UTC datetime."""
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class FrozenClock(ClockPort):
    """Test clock returning a fixed or artificially advanced datetime."""
    def __init__(self, fixed_time: datetime):
        self._current_time = fixed_time

    def now(self) -> datetime:
        return self._current_time

    def set_time(self, new_time: datetime) -> None:
        self._current_time = new_time
