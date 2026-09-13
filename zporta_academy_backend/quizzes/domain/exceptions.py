"""
Domain exceptions for Quizzes.
"""
from core.shared_kernel.domain.exceptions import DomainException


class QuizNotFoundError(DomainException):
    def __init__(self, identifier: str):
        super().__init__(f"Quiz '{identifier}' was not found.")


class QuestionNotFoundError(DomainException):
    def __init__(self, identifier: str):
        super().__init__(f"Question '{identifier}' was not found.")


class QuizAccessDeniedError(DomainException):
    def __init__(self, message: str = "Access to this quiz is denied."):
        super().__init__(message)


class InvalidQuizAnswerError(DomainException):
    def __init__(self, message: str = "Submitted answer data is invalid."):
        super().__init__(message)
