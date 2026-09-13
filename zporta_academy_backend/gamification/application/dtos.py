from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class ActivityLogCommand:
    user_id: int
    activity_type: str
    unique_key: str
    content_type_id: Optional[int] = None
    object_id: Optional[int] = None
    is_mistake: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    time_spent_seconds: Optional[int] = None


@dataclass
class UserScoreDTO:
    user_id: int
    total_points: int
    lessons_completed: int
    courses_completed: int
    correct_answers: int
    last_calculated: Optional[datetime] = None
