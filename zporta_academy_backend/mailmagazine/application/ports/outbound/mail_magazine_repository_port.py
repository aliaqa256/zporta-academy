from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from mailmagazine.domain.entities import (
    TeacherMailMagazineEntity,
    MailMagazineIssueEntity,
    MailMagazineTemplateEntity,
    RecipientGroupEntity,
    RecipientInfo,
)


class MailMagazineRepositoryPort(ABC):
    """Abstract port for mail magazine persistence."""

    @abstractmethod
    def get_magazine_by_id(self, magazine_id: int) -> Optional[TeacherMailMagazineEntity]:
        """Fetch teacher mail magazine by ID."""
        pass

    @abstractmethod
    def get_issue_by_id(self, issue_id: int) -> Optional[MailMagazineIssueEntity]:
        """Fetch mail magazine issue by ID."""
        pass

    @abstractmethod
    def get_teacher_followers_with_optin(self, teacher_id: int) -> List[RecipientInfo]:
        """Fetch all followers/attendees of teacher with mail magazine opt-in status."""
        pass

    @abstractmethod
    def create_issue(
        self,
        magazine_id: int,
        title: str,
        subject: str,
        html_content: str,
        recipient_ids: List[int],
        is_public: bool = False
    ) -> MailMagazineIssueEntity:
        """Create and persist a new sent issue archive."""
        pass

    @abstractmethod
    def update_magazine_sent_stats(self, magazine_id: int) -> None:
        """Increment times_sent and set last_sent_at on magazine."""
        pass

    @abstractmethod
    def list_teacher_issues(
        self,
        teacher_id: int,
        user_id: Optional[int] = None,
        is_staff: bool = False
    ) -> List[MailMagazineIssueEntity]:
        """List accessible issues by teacher."""
        pass
