from .dtos import (
    MailIssueDetailDTO,
    SendMagazineCommand,
    SendMagazineResultDTO,
    RecipientDTO,
    MailTemplateDTO,
)
from .use_cases.get_issue_detail import GetMailIssueDetailUseCase
from .use_cases.dispatch_issue import DispatchMailMagazineUseCase

__all__ = [
    "MailIssueDetailDTO",
    "SendMagazineCommand",
    "SendMagazineResultDTO",
    "RecipientDTO",
    "MailTemplateDTO",
    "GetMailIssueDetailUseCase",
    "DispatchMailMagazineUseCase",
]
