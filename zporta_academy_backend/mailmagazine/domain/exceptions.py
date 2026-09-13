class MailMagazineDomainError(Exception):
    """Base domain exception for mail magazine subsystem."""
    pass


class MailMagazineAccessDeniedError(MailMagazineDomainError):
    """Raised when a user attempts to view a gated issue without permission."""
    pass


class MailMagazineIssueNotFoundError(MailMagazineDomainError):
    """Raised when an issue cannot be found."""
    pass


class NoEligibleRecipientsError(MailMagazineDomainError):
    """Raised when attempting to dispatch a magazine without eligible recipients."""
    pass


class InvalidTemplateError(MailMagazineDomainError):
    """Raised when a template structure or content is invalid."""
    pass
