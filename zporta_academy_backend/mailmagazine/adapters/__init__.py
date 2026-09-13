from .outbound.persistence.django_mail_magazine_repository import DjangoMailMagazineRepository
from .outbound.email.django_email_sender import DjangoEmailSenderAdapter

__all__ = [
    "DjangoMailMagazineRepository",
    "DjangoEmailSenderAdapter",
]
