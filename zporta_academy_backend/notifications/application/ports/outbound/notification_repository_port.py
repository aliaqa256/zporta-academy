from abc import ABC, abstractmethod
from typing import Optional, List
from notifications.domain.entities import NotificationEntity, FCMTokenEntity


class NotificationRepositoryPort(ABC):
    """Abstract port for notification storage."""

    @abstractmethod
    def create_in_app_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        link: Optional[str] = None
    ) -> NotificationEntity:
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    def list_user_notifications(self, user_id: int, limit: int = 50) -> List[NotificationEntity]:
        pass
