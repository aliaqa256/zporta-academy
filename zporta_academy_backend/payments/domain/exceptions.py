"""
Payments Domain Exceptions.
"""
from core.shared_kernel.domain.exceptions import DomainException, EntityNotFoundError


class PaymentError(DomainException):
    """Base exception for payment domain errors."""
    pass


class InvalidPaymentAmountError(PaymentError):
    """Raised when payment amount is negative or zero."""
    pass


class PaymentGatewayError(PaymentError):
    """Raised when external payment gateway fails."""
    pass


class PromoCodeInvalidError(PaymentError):
    """Raised when a promo code is inactive, expired, or invalid."""
    pass
