import re
from typing import Optional
from ..dtos import SendMagazineCommand, SendMagazineResultDTO
from ..ports.outbound.mail_magazine_repository_port import MailMagazineRepositoryPort
from ..ports.outbound.email_sender_port import EmailSenderPort
from ...domain.policies import (
    RecipientEligibilityPolicy,
    TemplateRenderingPolicy,
)
from ...domain.exceptions import (
    MailMagazineDomainError,
    NoEligibleRecipientsError,
    MailMagazineAccessDeniedError,
)


class DispatchMailMagazineUseCase:
    """Orchestrates recipient resolution, template rendering, and bulk email dispatch."""

    def __init__(
        self,
        repository: MailMagazineRepositoryPort,
        email_sender: EmailSenderPort
    ):
        self.repository = repository
        self.email_sender = email_sender

    def execute(self, cmd: SendMagazineCommand) -> SendMagazineResultDTO:
        magazine = self.repository.get_magazine_by_id(cmd.magazine_id)
        if not magazine:
            raise MailMagazineDomainError(f"Magazine #{cmd.magazine_id} not found.")

        if magazine.teacher_id != cmd.teacher_id:
            raise MailMagazineAccessDeniedError("You do not have permission to send this mail magazine.")

        # Resolve candidate followers
        candidates = self.repository.get_teacher_followers_with_optin(cmd.teacher_id)
        
        # If magazine has pre-selected recipients, prefer them
        filter_ids = cmd.filter_recipient_ids or magazine.selected_recipient_ids
        eligible = RecipientEligibilityPolicy.filter_eligible_recipients(
            candidates=candidates,
            filter_ids=filter_ids if filter_ids else None
        )

        if not eligible:
            raise NoEligibleRecipientsError(
                "No eligible recipients found. Please select recipients or ensure followers have opted in."
            )

        recipient_ids = [r.id for r in eligible]

        # Create archive issue record
        issue = self.repository.create_issue(
            magazine_id=cmd.magazine_id,
            title=magazine.title,
            subject=magazine.subject,
            html_content=magazine.body,
            recipient_ids=recipient_ids,
            is_public=False
        )

        view_url = f"{cmd.site_url}/mail-magazines/{issue.id}"

        # Dispatch emails
        sent_count = 0
        for recipient in eligible:
            variables = {
                'student_name': recipient.full_name or recipient.username,
                'student_username': recipient.username,
                'teacher_name': cmd.teacher_username,
                'teacher_username': cmd.teacher_username,
                'course_name': '',
                'course_title': '',
                'site_url': cmd.site_url,
            }

            personalized_subject = TemplateRenderingPolicy.render_placeholders(magazine.subject, variables)
            personalized_html = TemplateRenderingPolicy.render_placeholders(magazine.body, variables)

            wrapper_html = TemplateRenderingPolicy.build_email_html_wrapper(
                site_name=cmd.site_name,
                site_url=cmd.site_url,
                site_logo=cmd.site_logo_url,
                view_in_browser_url=view_url,
                content_html=personalized_html
            )

            # Strip HTML for plain text fallback
            plain_text = re.sub(r'<[^>]+>', ' ', personalized_html).strip()

            success = self.email_sender.send_multipart_email(
                to_email=recipient.email,
                subject=personalized_subject,
                plain_text=plain_text,
                html_content=wrapper_html,
                from_name=cmd.site_name,
                fail_silently=True
            )
            if success:
                sent_count += 1

        # Update magazine metrics
        self.repository.update_magazine_sent_stats(cmd.magazine_id)

        return SendMagazineResultDTO(
            success=True,
            message=f"Email sent successfully to {len(recipient_ids)} recipients.",
            recipients_count=len(recipient_ids),
            issue_id=issue.id
        )
