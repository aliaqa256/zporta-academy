"""
Payments Domain Entities.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from core.shared_kernel.domain.base_entity import BaseEntity
from payments.domain.value_objects import Currency, PaymentStatus


@dataclass(eq=False)
class PaymentEntity(BaseEntity[Optional[int]]):
    """Represents a payment transaction record."""
    id: Optional[int] = None
    user_id: int = 0
    course_id: int = 0
    stripe_payment_id: str = ""
    amount_cents: int = 0
    currency: Currency = Currency.USD
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: Optional[datetime] = None

    def is_successful(self) -> bool:
        return self.status == PaymentStatus.SUCCEEDED


@dataclass(frozen=True)
class PromoCodeEntity:
    """Represents a promotional discount code."""
    code: str
    discount_percent: int
    is_active: bool = True
    max_uses: Optional[int] = None
    current_uses: int = 0
