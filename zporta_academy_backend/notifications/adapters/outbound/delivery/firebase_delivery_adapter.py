from typing import Dict, Any, Optional
from django.contrib.auth import get_user_model
from notifications.application.ports.outbound.notification_delivery_port import NotificationDeliveryPort
from notifications.utils import send_push_to_user_devices

User = get_user_model()


class FirebaseDeliveryAdapter(NotificationDeliveryPort):
    """Adapter invoking Firebase Cloud Messaging."""

    def deliver_push_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        link: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> int:
        user = User.objects.filter(id=user_id).first()
        if not user:
            return 0
        try:
            return send_push_to_user_devices(
                user=user,
                title=title,
                body=message,
                link=link,
                extra_data=extra_data
            )
        except Exception:
            return 0
