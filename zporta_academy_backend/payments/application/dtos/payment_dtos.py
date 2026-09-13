"""
Payments Application DTOs.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class CreateCheckoutCommand:
    user_id: int
    course_id: int
    amount_cents: int
    currency: str = "usd"
    promo_code: Optional[str] = None
    success_url: str = ""
    cancel_url: str = ""


@dataclass(frozen=True)
class CheckoutSessionDTO:
    session_id: str
    checkout_url: str
    amount_cents: int
    currency: str


@dataclass(frozen=True)
class ConfirmPaymentCommand:
    session_id: str
    user_id: int


@dataclass(frozen=True)
class PaymentResultDTO:
    id: int
    user_id: int
    course_id: int
    stripe_payment_id: str
    amount_cents: int
    currency: str
    status: str
    created_at: Optional[datetime] = None
