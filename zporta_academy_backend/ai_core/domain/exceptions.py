"""
Domain exceptions for AI Core.
"""
from core.shared_kernel.domain.exceptions import DomainException


class AIProviderError(DomainException):
    def __init__(self, message: str = "AI Provider error occurred."):
        super().__init__(message)


class AIProviderUnavailableError(DomainException):
    def __init__(self, provider: str):
        super().__init__(f"AI Provider '{provider}' is currently unavailable or misconfigured.")


class AIQuotaExceededError(DomainException):
    def __init__(self, provider: str):
        super().__init__(f"Quota or rate limit exceeded for AI provider '{provider}'.")


class InvalidAIRequestError(DomainException):
    def __init__(self, message: str = "Invalid AI request parameters."):
        super().__init__(message)
