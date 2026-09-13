from ..application.ports.outbound.mail_magazine_repository_port import MailMagazineRepositoryPort
from ..application.ports.outbound.email_sender_port import EmailSenderPort
from ..application.use_cases.get_issue_detail import GetMailIssueDetailUseCase
from ..application.use_cases.dispatch_issue import DispatchMailMagazineUseCase
from ..adapters.outbound.persistence.django_mail_magazine_repository import DjangoMailMagazineRepository
from ..adapters.outbound.email.django_email_sender import DjangoEmailSenderAdapter


def build_mail_magazine_repository() -> MailMagazineRepositoryPort:
    return DjangoMailMagazineRepository()


def build_email_sender() -> EmailSenderPort:
    return DjangoEmailSenderAdapter()


def build_get_mail_issue_detail_use_case(
    repository: MailMagazineRepositoryPort = None
) -> GetMailIssueDetailUseCase:
    return GetMailIssueDetailUseCase(
        repository=repository or build_mail_magazine_repository()
    )


def build_dispatch_mail_magazine_use_case(
    repository: MailMagazineRepositoryPort = None,
    email_sender: EmailSenderPort = None
) -> DispatchMailMagazineUseCase:
    return DispatchMailMagazineUseCase(
        repository=repository or build_mail_magazine_repository(),
        email_sender=email_sender or build_email_sender()
    )
