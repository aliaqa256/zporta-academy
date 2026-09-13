from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class RecipientInfo:
    """Represents a recipient user."""
    id: int
    username: str
    email: str
    full_name: str = ""
    display_name: str = ""
    mail_magazine_enabled: bool = True
    guide_status: str = "none"


@dataclass
class MailMagazineTemplateEntity:
    """Domain model for predefined email templates."""
    id: Optional[int]
    name: str
    template_type: str
    subject: str
    body: str
    created_by_id: int
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class TeacherMailMagazineEntity:
    """Domain model for a teacher's configured mail campaign."""
    id: Optional[int]
    teacher_id: int
    title: str
    subject: str
    body: str
    frequency: str = "one_time"
    template_id: Optional[int] = None
    is_active: bool = True
    send_at: Optional[datetime] = None
    last_sent_at: Optional[datetime] = None
    times_sent: int = 0
    selected_recipient_ids: List[int] = field(default_factory=list)


@dataclass
class MailMagazineIssueEntity:
    """Domain model for an archived mail issue."""
    id: Optional[int]
    magazine_id: int
    teacher_id: int
    title: str
    subject: str
    html_content: str
    sent_at: Optional[datetime] = None
    is_public: bool = False
    recipient_ids: List[int] = field(default_factory=list)


@dataclass
class RecipientGroupEntity:
    """Domain model for reusable recipient groups."""
    id: Optional[int]
    teacher_id: int
    name: str
    description: Optional[str] = None
    is_dynamic: bool = False
    linked_course_id: Optional[int] = None
    member_ids: List[int] = field(default_factory=list)
