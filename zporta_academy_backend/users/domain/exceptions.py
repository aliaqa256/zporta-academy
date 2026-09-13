"""
Domain exceptions for Users and Authentication.
Zero framework dependencies.
"""
from core.shared_kernel.domain.exceptions import DomainException


class UserNotFoundError(DomainException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"User '{identifier}' was not found.",
            code="USER_NOT_FOUND",
            details={"identifier": identifier}
        )


class InvalidCredentialsError(DomainException):
    def __init__(self, message: str = "Invalid username/email or password."):
        super().__init__(message=message, code="INVALID_CREDENTIALS")


class UsernameAlreadyTakenError(DomainException):
    def __init__(self, username: str):
        super().__init__(
            message="Username already taken.",
            code="USERNAME_TAKEN",
            details={"username": username}
        )


class EmailAlreadyRegisteredError(DomainException):
    def __init__(self, email: str):
        super().__init__(
            message="Email already registered.",
            code="EMAIL_REGISTERED",
            details={"email": email}
        )


class InvalidPasswordError(DomainException):
    def __init__(self, message: str):
        super().__init__(message=message, code="INVALID_PASSWORD")
