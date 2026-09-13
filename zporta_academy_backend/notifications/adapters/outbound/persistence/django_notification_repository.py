from typing import Optional, List
from notifications.domain.entities import NotificationEntity
from notifications.application.ports.outbound.notification_repository_port import NotificationRepositoryPort
from notifications.models import Notification


class DjangoNotificationRepository(NotificationRepositoryPort):
    """Django ORM implementation of NotificationRepositoryPort."""

    def create_in_app_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        link: Optional[str] = None
    ) -> NotificationEntity:
        notif = Notification.objects.create(
            user_id=user_id,
            title=title,
            message=message,
            link=link
        )
        return NotificationEntity(
            id=notif.id,
            user_id=notif.user_id,
            title=notif.title,
            message=notif.message,
            link=notif.link,
            is_read=notif.is_read,
            is_sent_push=notif.is_sent_push,
            created_at=notif.created_at
        )

    def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        updated = Notification.objects.filter(id=notification_id, user_id=user_id).update(is_read=True)
        return updated > 0

    def list_user_notifications(self, user_id: int, limit: int = 50) -> List[NotificationEntity]:
        qs = Notification.objects.filter(user_id=user_id).order_by('-created_at')[:limit]
        return [
            NotificationEntity(
                id=n.id,
                user_id=n.user_id,
                title=n.title,
                message=n.message,
                link=n.link,
                is_read=n.is_read,
                is_sent_push=n.is_sent_push,
                created_at=n.created_at
            )
            for n in qs
        ]
