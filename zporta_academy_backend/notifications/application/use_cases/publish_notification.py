from typing import Optional
from notifications.domain.policies import NotificationFormattingPolicy
from ..dtos import SendPushCommand, PushResultDTO
from ..ports.outbound.notification_repository_port import NotificationRepositoryPort
from ..ports.outbound.notification_delivery_port import NotificationDeliveryPort


class PublishNotificationUseCase:
    """Creates in-app notification record and dispatches push to user devices."""

    def __init__(
        self,
        repository: NotificationRepositoryPort,
        delivery: NotificationDeliveryPort
    ):
        self.repository = repository
        self.delivery = delivery

    def execute(self, cmd: SendPushCommand) -> PushResultDTO:
        title, message = NotificationFormattingPolicy.format_title_and_body(cmd.title, cmd.message)
        normalized_link = NotificationFormattingPolicy.normalize_link(cmd.link)

        # 1. Create in-app notification
        entity = self.repository.create_in_app_notification(
            user_id=cmd.user_id,
            title=title,
            message=message,
            link=cmd.link
        )

        # 2. Dispatch push notifications
        extra_data = {**cmd.extra_data, "notification_db_id": str(entity.id or "")}
        delivered = self.delivery.deliver_push_notification(
            user_id=cmd.user_id,
            title=title,
            message=message,
            link=normalized_link,
            extra_data=extra_data
        )

        return PushResultDTO(
            success=True,
            delivered_count=delivered,
            notification_id=entity.id
        )
