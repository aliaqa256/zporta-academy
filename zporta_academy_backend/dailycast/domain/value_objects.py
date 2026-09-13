"""
DailyCast Domain Value Objects.
"""
from enum import Enum


class PodcastStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class OutputFormat(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    BOTH = "both"


class ReplySize(str, Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    DETAILED = "detailed"


class MonthRange(str, Enum):
    CURRENT = "current"
    LAST_3 = "last_3"
    LAST_6 = "last_6"
    LAST_12 = "last_12"
    ALL = "all"
