from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class NotificationDTO:
    id: int
    user_id: int
    title: str
    message: str
    link: Optional[str]
    is_read: bool
    created_at: Optional[datetime]


@dataclass
class SendPushCommand:
    user_id: int
    title: str
    message: str
    link: Optional[str] = None
    extra_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PushResultDTO:
    success: bool
    delivered_count: int
    notification_id: Optional[int] = None
