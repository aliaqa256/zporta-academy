from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class NotificationDeliveryPort(ABC):
    """Abstract port for delivering external push notifications."""

    @abstractmethod
    def deliver_push_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        link: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> int:
        """Sends push notification to all user's active devices. Returns delivered count."""
        pass
