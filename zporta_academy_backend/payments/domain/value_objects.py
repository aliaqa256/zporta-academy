"""
Payments Domain Value Objects.
"""
from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"


class Currency(str, Enum):
    USD = "usd"
    JPY = "jpy"
    EUR = "eur"
