from notifications.application.ports.outbound.notification_repository_port import NotificationRepositoryPort
from notifications.application.ports.outbound.notification_delivery_port import NotificationDeliveryPort
from notifications.application.use_cases.publish_notification import PublishNotificationUseCase
from notifications.adapters.outbound.persistence.django_notification_repository import DjangoNotificationRepository
from notifications.adapters.outbound.delivery.firebase_delivery_adapter import FirebaseDeliveryAdapter


def build_notification_repository() -> NotificationRepositoryPort:
    return DjangoNotificationRepository()


def build_notification_delivery() -> NotificationDeliveryPort:
    return FirebaseDeliveryAdapter()


def build_publish_notification_use_case(
    repository: NotificationRepositoryPort = None,
    delivery: NotificationDeliveryPort = None
) -> PublishNotificationUseCase:
    return PublishNotificationUseCase(
        repository=repository or build_notification_repository(),
        delivery=delivery or build_notification_delivery()
    )
