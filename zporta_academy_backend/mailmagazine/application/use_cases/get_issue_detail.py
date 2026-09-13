from typing import Optional
from ..dtos import MailIssueDetailDTO
from ..ports.outbound.mail_magazine_repository_port import MailMagazineRepositoryPort
from ...domain.policies import GatedPreviewPolicy
from ...domain.exceptions import MailMagazineIssueNotFoundError, MailMagazineAccessDeniedError


class GetMailIssueDetailUseCase:
    """Retrieves a mail magazine issue and enforces gating preview rules."""

    def __init__(self, repository: MailMagazineRepositoryPort):
        self.repository = repository

    def execute(
        self,
        issue_id: int,
        requesting_user_id: Optional[int],
        is_staff: bool = False
    ) -> MailIssueDetailDTO:
        issue = self.repository.get_issue_by_id(issue_id)
        if not issue:
            raise MailMagazineIssueNotFoundError(f"Issue #{issue_id} not found.")

        is_teacher = requesting_user_id == issue.teacher_id
        is_authorized = GatedPreviewPolicy.can_view_full_issue(
            user_id=requesting_user_id,
            is_staff=is_staff,
            is_teacher=is_teacher,
            recipient_ids=issue.recipient_ids,
            is_public=issue.is_public
        )

        if not is_authorized and not issue.is_public:
            raise MailMagazineAccessDeniedError("You do not have permission to view this issue.")

        content = GatedPreviewPolicy.apply_content_gating(
            html_content=issue.html_content,
            is_authorized=is_authorized
        )

        return MailIssueDetailDTO(
            id=issue.id or issue_id,
            magazine_id=issue.magazine_id,
            teacher_id=issue.teacher_id,
            teacher_username="",  # Populated by adapter / view
            title=issue.title,
            subject=issue.subject,
            html_content=content,
            is_public=issue.is_public,
            is_gated=not is_authorized,
            sent_at=issue.sent_at,
            recipient_count=len(issue.recipient_ids)
        )
