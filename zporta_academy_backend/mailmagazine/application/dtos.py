from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class MailIssueDetailDTO:
    id: int
    magazine_id: int
    teacher_id: int
    teacher_username: str
    title: str
    subject: str
    html_content: str
    is_public: bool
    is_gated: bool
    sent_at: Optional[datetime]
    recipient_count: int = 0


@dataclass
class SendMagazineCommand:
    magazine_id: int
    teacher_id: int
    teacher_username: str
    site_url: str = "https://zportaacademy.com"
    site_name: str = "Zporta Academy"
    site_logo_url: str = "https://zportaacademy.com/logo.png"
    filter_recipient_ids: Optional[List[int]] = None


@dataclass
class SendMagazineResultDTO:
    success: bool
    message: str
    recipients_count: int
    issue_id: Optional[int] = None


@dataclass
class RecipientDTO:
    id: int
    username: str
    email: str
    display_name: str
    full_name: str
    guide_status: str
    email_enabled: bool


@dataclass
class MailTemplateDTO:
    id: Optional[int]
    name: str
    template_type: str
    subject: str
    body: str
    created_by_id: int
    is_active: bool = True
