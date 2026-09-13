from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List, Dict, Any


@dataclass
class ActivityEntity:
    id: Optional[int]
    user_id: int
    activity_type: str
    points: int
    unique_key: str
    is_mistake: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    time_spent_seconds: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class UserScoreEntity:
    user_id: int
    total_points: int = 0
    lessons_completed: int = 0
    courses_completed: int = 0
    correct_answers: int = 0
    last_calculated: Optional[datetime] = None
