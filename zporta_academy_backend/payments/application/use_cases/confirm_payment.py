"""
Confirm Payment Use Case.
"""
from datetime import datetime, timezone
from payments.application.dtos.payment_dtos import ConfirmPaymentCommand, PaymentResultDTO
from payments.application.ports.outbound.payment_gateway_port import PaymentGatewayPort
from payments.application.ports.outbound.payment_repository_port import PaymentRepositoryPort
from payments.domain.entities import PaymentEntity
from payments.domain.value_objects import Currency, PaymentStatus


class ConfirmPaymentUseCase:
    """Use case to verify completed checkout session and record payment transaction."""

    def __init__(self, gateway: PaymentGatewayPort, repository: PaymentRepositoryPort):
        self._gateway = gateway
        self._repository = repository

    def execute(self, cmd: ConfirmPaymentCommand) -> PaymentResultDTO:
        session_data = self._gateway.verify_session(cmd.session_id)

        course_id = int(session_data.get("course_id", 0))
        amount_cents = int(session_data.get("amount_cents", 0))
        currency_str = session_data.get("currency", "usd")
        currency = Currency(currency_str) if currency_str in Currency._value2member_map_ else Currency.USD

        existing = self._repository.get_by_stripe_id(cmd.session_id)
        if existing:
            return PaymentResultDTO(
                id=existing.id or 0,
                user_id=existing.user_id,
                course_id=existing.course_id,
                stripe_payment_id=existing.stripe_payment_id,
                amount_cents=existing.amount_cents,
                currency=existing.currency.value,
                status=existing.status.value,
                created_at=existing.created_at,
            )

        payment = PaymentEntity(
            user_id=cmd.user_id,
            course_id=course_id,
            stripe_payment_id=cmd.session_id,
            amount_cents=amount_cents,
            currency=currency,
            status=PaymentStatus.SUCCEEDED,
            created_at=datetime.now(timezone.utc),
        )

        saved = self._repository.save_payment(payment)

        return PaymentResultDTO(
            id=saved.id or 0,
            user_id=saved.user_id,
            course_id=saved.course_id,
            stripe_payment_id=saved.stripe_payment_id,
            amount_cents=saved.amount_cents,
            currency=saved.currency.value,
            status=saved.status.value,
            created_at=saved.created_at,
        )
