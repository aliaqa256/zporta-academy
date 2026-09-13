"""
Django Payment Repository Persistence Adapter.
"""
from typing import List, Optional
from payments.application.ports.outbound.payment_repository_port import PaymentRepositoryPort
from payments.domain.entities import PaymentEntity, PromoCodeEntity
from payments.domain.value_objects import Currency, PaymentStatus
from payments.models import Payment


class DjangoPaymentRepository(PaymentRepositoryPort):
    """PostgreSQL / SQLite persistence adapter for Payment transactions."""

    def _to_entity(self, model: Payment) -> PaymentEntity:
        return PaymentEntity(
            id=model.id,
            user_id=model.user_id,
            course_id=model.course_id,
            stripe_payment_id=model.stripe_payment_id,
            amount_cents=model.amount,
            currency=Currency(model.currency) if model.currency in Currency._value2member_map_ else Currency.USD,
            status=PaymentStatus.SUCCEEDED if model.status == "succeeded" else PaymentStatus.PENDING,
            created_at=model.created_at,
        )

    def save_payment(self, payment: PaymentEntity) -> PaymentEntity:
        if payment.id:
            model = Payment.objects.get(pk=payment.id)
        else:
            model = Payment(
                user_id=payment.user_id,
                course_id=payment.course_id,
                stripe_payment_id=payment.stripe_payment_id,
            )

        model.amount = payment.amount_cents
        model.currency = payment.currency.value
        model.status = payment.status.value
        model.save()
        return self._to_entity(model)

    def get_by_stripe_id(self, stripe_payment_id: str) -> Optional[PaymentEntity]:
        try:
            m = Payment.objects.get(stripe_payment_id=stripe_payment_id)
            return self._to_entity(m)
        except Payment.DoesNotExist:
            return None

    def list_user_payments(self, user_id: int) -> List[PaymentEntity]:
        qs = Payment.objects.filter(user_id=user_id).order_by("-created_at")
        return [self._to_entity(m) for m in qs]

    def get_promo_code(self, code: str) -> Optional[PromoCodeEntity]:
        # Return promo entity or None (matches in-memory / cache promo codes)
        clean_code = (code or "").upper().strip()
        if clean_code == "WELCOME10":
            return PromoCodeEntity(code="WELCOME10", discount_percent=10, is_active=True)
        elif clean_code == "VIP50":
            return PromoCodeEntity(code="VIP50", discount_percent=50, is_active=True)
        return None
