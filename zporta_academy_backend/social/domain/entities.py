from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class GuideRequestStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


@dataclass
class GuideRequestEntity:
    id: Optional[int]
    explorer_id: int
    guide_id: int
    status: GuideRequestStatus = GuideRequestStatus.PENDING
    created_at: Optional[datetime] = None


@dataclass
class ConnectedUserCardEntity:
    id: int
    username: str
    display_name: str
    profile_picture_url: Optional[str] = None
