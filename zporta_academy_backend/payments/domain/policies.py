"""
Payments Domain Policies.
"""
from typing import Optional
from payments.domain.entities import PromoCodeEntity
from payments.domain.exceptions import InvalidPaymentAmountError, PromoCodeInvalidError


class PaymentValidationPolicy:
    """Validates payment transactions and promo code calculations."""

    @staticmethod
    def validate_amount(amount_cents: int) -> None:
        if amount_cents <= 0:
            raise InvalidPaymentAmountError(f"Payment amount must be greater than zero. Received: {amount_cents}")

    @staticmethod
    def apply_promo_code(original_amount_cents: int, promo: Optional[PromoCodeEntity]) -> int:
        if not promo:
            return original_amount_cents

        if not promo.is_active:
            raise PromoCodeInvalidError(f"Promo code '{promo.code}' is inactive.")

        if promo.max_uses and promo.current_uses >= promo.max_uses:
            raise PromoCodeInvalidError(f"Promo code '{promo.code}' has reached maximum usage limit.")

        discount = int(original_amount_cents * (promo.discount_percent / 100.0))
        return max(0, original_amount_cents - discount)
