from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NotificationEntity:
    id: Optional[int]
    user_id: int
    title: str
    message: str
    link: Optional[str] = None
    is_read: bool = False
    is_sent_push: bool = False
    created_at: Optional[datetime] = None


@dataclass
class FCMTokenEntity:
    id: Optional[int]
    user_id: int
    device_id: str
    token: str
    is_active: bool = True
