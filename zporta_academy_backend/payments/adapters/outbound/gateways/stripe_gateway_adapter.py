"""
Stripe Payment Gateway Adapter.
"""
import logging
import uuid
from typing import Any, Dict
from django.conf import settings
from payments.application.dtos.payment_dtos import CheckoutSessionDTO, CreateCheckoutCommand
from payments.application.ports.outbound.payment_gateway_port import PaymentGatewayPort
from payments.domain.exceptions import PaymentGatewayError

logger = logging.getLogger(__name__)


class StripeGatewayAdapter(PaymentGatewayPort):
    """Integrates Stripe Checkout with graceful mock fallback for dev/test environments."""

    def create_checkout_session(self, cmd: CreateCheckoutCommand) -> CheckoutSessionDTO:
        stripe_api_key = getattr(settings, "STRIPE_SECRET_KEY", None)

        if not stripe_api_key:
            # Mock session for dev environment
            session_id = f"cs_test_{uuid.uuid4().hex}"
            checkout_url = f"https://checkout.stripe.com/c/pay/{session_id}"
            return CheckoutSessionDTO(
                session_id=session_id,
                checkout_url=checkout_url,
                amount_cents=cmd.amount_cents,
                currency=cmd.currency,
            )

        try:
            import stripe
            stripe.api_key = stripe_api_key

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": cmd.currency,
                        "unit_amount": cmd.amount_cents,
                        "product_data": {
                            "name": f"Course Access #{cmd.course_id}",
                        },
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=cmd.success_url or "http://localhost:3000/payments/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=cmd.cancel_url or "http://localhost:3000/payments/cancel",
                metadata={
                    "user_id": str(cmd.user_id),
                    "course_id": str(cmd.course_id),
                },
            )

            return CheckoutSessionDTO(
                session_id=session.id,
                checkout_url=session.url,
                amount_cents=cmd.amount_cents,
                currency=cmd.currency,
            )
        except Exception as e:
            logger.error(f"Stripe session creation failed: {e}")
            raise PaymentGatewayError(f"Stripe gateway error: {e}") from e

    def verify_session(self, session_id: str) -> Dict[str, Any]:
        stripe_api_key = getattr(settings, "STRIPE_SECRET_KEY", None)

        if not stripe_api_key or session_id.startswith("cs_test_"):
            return {
                "session_id": session_id,
                "amount_cents": 1999,
                "currency": "usd",
                "status": "paid",
            }

        try:
            import stripe
            stripe.api_key = stripe_api_key
            session = stripe.checkout.Session.retrieve(session_id)
            return {
                "session_id": session.id,
                "amount_cents": session.amount_total,
                "currency": session.currency,
                "status": session.payment_status,
                "course_id": session.metadata.get("course_id"),
                "user_id": session.metadata.get("user_id"),
            }
        except Exception as e:
            logger.error(f"Stripe session verification failed: {e}")
            raise PaymentGatewayError(f"Stripe verification error: {e}") from e
