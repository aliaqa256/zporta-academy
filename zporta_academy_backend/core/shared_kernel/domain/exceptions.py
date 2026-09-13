"""
Base domain exceptions for Zporta Academy backend.
Zero framework dependencies.
"""
from typing import Optional, Dict, Any


class DomainException(Exception):
    """Base exception for all domain rule violations."""
    def __init__(self, message: str, code: str = "DOMAIN_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class EntityNotFoundError(DomainException):
    """Raised when an entity is not found by ID or lookup key."""
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            message=f"{entity_name} with identifier '{entity_id}' not found.",
            code="ENTITY_NOT_FOUND",
            details={"entity_name": entity_name, "entity_id": str(entity_id)}
        )


class InvariantViolationError(DomainException):
    """Raised when a business invariant or rule is violated."""
    def __init__(self, message: str, code: str = "INVARIANT_VIOLATION", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code=code, details=details)


class UnauthorizedDomainActionError(DomainException):
    """Raised when an actor lacks permission to execute a domain action."""
    def __init__(self, message: str = "Unauthorized domain action", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, code="UNAUTHORIZED_ACTION", details=details)
