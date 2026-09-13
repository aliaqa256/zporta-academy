"""
Payment Repository Outbound Port Interface.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from payments.domain.entities import PaymentEntity, PromoCodeEntity


class PaymentRepositoryPort(ABC):
    """Outbound port for persisting and querying payment transactions and promo codes."""

    @abstractmethod
    def save_payment(self, payment: PaymentEntity) -> PaymentEntity:
        """Persist or update payment transaction."""
        pass

    @abstractmethod
    def get_by_stripe_id(self, stripe_payment_id: str) -> Optional[PaymentEntity]:
        """Fetch payment by Stripe payment identifier."""
        pass

    @abstractmethod
    def list_user_payments(self, user_id: int) -> List[PaymentEntity]:
        """Fetch all payments for a user."""
        pass

    @abstractmethod
    def get_promo_code(self, code: str) -> Optional[PromoCodeEntity]:
        """Fetch promo code details."""
        pass
