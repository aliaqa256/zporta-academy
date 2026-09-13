"""
Payments Composition Container.
"""
from payments.adapters.outbound.gateways.stripe_gateway_adapter import StripeGatewayAdapter
from payments.adapters.outbound.persistence.django_payment_repository import DjangoPaymentRepository
from payments.application.ports.outbound.payment_gateway_port import PaymentGatewayPort
from payments.application.ports.outbound.payment_repository_port import PaymentRepositoryPort
from payments.application.use_cases.confirm_payment import ConfirmPaymentUseCase
from payments.application.use_cases.process_checkout import ProcessCheckoutUseCase


def build_payment_repository() -> PaymentRepositoryPort:
    return DjangoPaymentRepository()


def build_payment_gateway() -> PaymentGatewayPort:
    return StripeGatewayAdapter()


def build_process_checkout_use_case(
    gateway: PaymentGatewayPort = None,
    repository: PaymentRepositoryPort = None,
) -> ProcessCheckoutUseCase:
    return ProcessCheckoutUseCase(
        gateway=gateway or build_payment_gateway(),
        repository=repository or build_payment_repository(),
    )


def build_confirm_payment_use_case(
    gateway: PaymentGatewayPort = None,
    repository: PaymentRepositoryPort = None,
) -> ConfirmPaymentUseCase:
    return ConfirmPaymentUseCase(
        gateway=gateway or build_payment_gateway(),
        repository=repository or build_payment_repository(),
    )
