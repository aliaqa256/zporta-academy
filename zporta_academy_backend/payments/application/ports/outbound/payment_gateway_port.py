"""
Payment Gateway Outbound Port Interface.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from payments.application.dtos.payment_dtos import CheckoutSessionDTO, CreateCheckoutCommand


class PaymentGatewayPort(ABC):
    """Outbound port for communicating with payment gateways (e.g. Stripe)."""

    @abstractmethod
    def create_checkout_session(self, cmd: CreateCheckoutCommand) -> CheckoutSessionDTO:
        """Create a hosted checkout session."""
        pass

    @abstractmethod
    def verify_session(self, session_id: str) -> Dict[str, Any]:
        """Verify checkout session completion and extract metadata."""
        pass
