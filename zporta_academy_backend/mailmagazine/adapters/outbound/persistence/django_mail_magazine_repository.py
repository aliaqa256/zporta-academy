from typing import Optional, List
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from mailmagazine.application.ports.outbound.mail_magazine_repository_port import MailMagazineRepositoryPort
from mailmagazine.domain.entities import (
    TeacherMailMagazineEntity,
    MailMagazineIssueEntity,
    RecipientInfo,
)
from mailmagazine.models import TeacherMailMagazine, MailMagazineIssue
from social.models import GuideRequest

User = get_user_model()


class DjangoMailMagazineRepository(MailMagazineRepositoryPort):
    """Django ORM implementation of MailMagazineRepositoryPort."""

    def get_magazine_by_id(self, magazine_id: int) -> Optional[TeacherMailMagazineEntity]:
        try:
            m = TeacherMailMagazine.objects.prefetch_related('selected_recipients').get(id=magazine_id)
            selected_ids = list(m.selected_recipients.values_list('id', flat=True))
            return TeacherMailMagazineEntity(
                id=m.id,
                teacher_id=m.teacher_id,
                title=m.title,
                subject=m.subject,
                body=m.body,
                frequency=m.frequency,
                template_id=m.template_id,
                is_active=m.is_active,
                send_at=m.send_at,
                last_sent_at=m.last_sent_at,
                times_sent=m.times_sent,
                selected_recipient_ids=selected_ids
            )
        except TeacherMailMagazine.DoesNotExist:
            return None

    def get_issue_by_id(self, issue_id: int) -> Optional[MailMagazineIssueEntity]:
        try:
            issue = MailMagazineIssue.objects.select_related('magazine', 'magazine__teacher').prefetch_related('recipients').get(id=issue_id)
            recipient_ids = list(issue.recipients.values_list('id', flat=True))
            return MailMagazineIssueEntity(
                id=issue.id,
                magazine_id=issue.magazine_id,
                teacher_id=issue.magazine.teacher_id,
                title=issue.title,
                subject=issue.subject,
                html_content=issue.html_content,
                sent_at=issue.sent_at,
                is_public=issue.is_public,
                recipient_ids=recipient_ids
            )
        except MailMagazineIssue.DoesNotExist:
            return None

    def get_teacher_followers_with_optin(self, teacher_id: int) -> List[RecipientInfo]:
        guide_requests = GuideRequest.objects.filter(
            guide_id=teacher_id,
            status='accepted'
        ).select_related('explorer', 'explorer__profile')

        recipients: List[RecipientInfo] = []
        for gr in guide_requests:
            u = gr.explorer
            profile = getattr(u, 'profile', None)
            enabled = getattr(profile, 'mail_magazine_enabled', True) if profile else True
            display_name = getattr(profile, 'display_name', u.username) if profile else u.username
            full_name = f"{u.first_name} {u.last_name}".strip() or u.username
            
            recipients.append(
                RecipientInfo(
                    id=u.id,
                    username=u.username,
                    email=u.email,
                    full_name=full_name,
                    display_name=display_name,
                    mail_magazine_enabled=enabled,
                    guide_status=gr.status
                )
            )
        return recipients

    def create_issue(
        self,
        magazine_id: int,
        title: str,
        subject: str,
        html_content: str,
        recipient_ids: List[int],
        is_public: bool = False
    ) -> MailMagazineIssueEntity:
        issue = MailMagazineIssue.objects.create(
            magazine_id=magazine_id,
            title=title,
            subject=subject,
            html_content=html_content,
            is_public=is_public
        )
        if recipient_ids:
            issue.recipients.set(recipient_ids)

        return MailMagazineIssueEntity(
            id=issue.id,
            magazine_id=issue.magazine_id,
            teacher_id=issue.magazine.teacher_id,
            title=issue.title,
            subject=issue.subject,
            html_content=issue.html_content,
            sent_at=issue.sent_at,
            is_public=issue.is_public,
            recipient_ids=recipient_ids
        )

    def update_magazine_sent_stats(self, magazine_id: int) -> None:
        try:
            m = TeacherMailMagazine.objects.get(id=magazine_id)
            m.last_sent_at = timezone.now()
            m.times_sent += 1
            m.save(update_fields=['last_sent_at', 'times_sent'])
        except TeacherMailMagazine.DoesNotExist:
            pass

    def list_teacher_issues(
        self,
        teacher_id: int,
        user_id: Optional[int] = None,
        is_staff: bool = False
    ) -> List[MailMagazineIssueEntity]:
        qs = MailMagazineIssue.objects.filter(magazine__teacher_id=teacher_id).select_related('magazine').prefetch_related('recipients')
        
        if user_id != teacher_id and not is_staff:
            qs = qs.filter(Q(recipients__id=user_id) | Q(is_public=True)).distinct()

        results = []
        for issue in qs:
            rec_ids = list(issue.recipients.values_list('id', flat=True))
            results.append(
                MailMagazineIssueEntity(
                    id=issue.id,
                    magazine_id=issue.magazine_id,
                    teacher_id=issue.magazine.teacher_id,
                    title=issue.title,
                    subject=issue.subject,
                    html_content=issue.html_content,
                    sent_at=issue.sent_at,
                    is_public=issue.is_public,
                    recipient_ids=rec_ids
                )
            )
        return results
