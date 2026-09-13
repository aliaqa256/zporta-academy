"""
Process Checkout Use Case.
"""
from payments.application.dtos.payment_dtos import CheckoutSessionDTO, CreateCheckoutCommand
from payments.application.ports.outbound.payment_gateway_port import PaymentGatewayPort
from payments.application.ports.outbound.payment_repository_port import PaymentRepositoryPort
from payments.domain.policies import PaymentValidationPolicy


class ProcessCheckoutUseCase:
    """Use case to validate checkout requests, apply discounts, and generate Stripe sessions."""

    def __init__(self, gateway: PaymentGatewayPort, repository: PaymentRepositoryPort):
        self._gateway = gateway
        self._repository = repository

    def execute(self, cmd: CreateCheckoutCommand) -> CheckoutSessionDTO:
        PaymentValidationPolicy.validate_amount(cmd.amount_cents)

        final_amount = cmd.amount_cents
        if cmd.promo_code:
            promo = self._repository.get_promo_code(cmd.promo_code)
            final_amount = PaymentValidationPolicy.apply_promo_code(cmd.amount_cents, promo)

        adjusted_cmd = CreateCheckoutCommand(
            user_id=cmd.user_id,
            course_id=cmd.course_id,
            amount_cents=final_amount,
            currency=cmd.currency,
            promo_code=cmd.promo_code,
            success_url=cmd.success_url,
            cancel_url=cmd.cancel_url,
        )

        return self._gateway.create_checkout_session(adjusted_cmd)
