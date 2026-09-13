from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GuideRequestDTO:
    id: int
    explorer_id: int
    explorer_username: str
    guide_id: int
    guide_username: str
    status: str
    created_at: Optional[datetime] = None


@dataclass
class ConnectedUserDTO:
    id: int
    username: str
    display_name: str
    profile_picture_url: Optional[str] = None
