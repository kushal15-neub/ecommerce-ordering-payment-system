from abc import ABC, abstractmethod
import uuid

import stripe

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, amount):
        pass


class StripePaymentStrategy(PaymentStrategy):

    def pay(self, amount):

        payment_intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),
            currency="usd",
            automatic_payment_methods={
                "enabled": True
            }
        )

        return {
            "provider": "stripe",
            "transaction_id": payment_intent.id,
            "client_secret": payment_intent.client_secret,
            "status": "pending",
            "amount": float(amount),
            "raw_response": {
                "id": payment_intent.id,
                "status": payment_intent.status,
                "client_secret": payment_intent.client_secret,
                "amount": payment_intent.amount,
                "currency": payment_intent.currency,
            }
        }


class BkashPaymentStrategy(PaymentStrategy):
    """
    Mock bKash strategy. Real sandbox/live APIs require
    bKash merchant credentials.
    """

    def pay(self, amount):

        transaction_id = (
            f"BKASH-{uuid.uuid4().hex[:12].upper()}"
        )

        return {
            "provider": "bkash",
            "transaction_id": transaction_id,
            "status": "pending",
            "amount": float(amount),
            "message": (
                "Mock bKash payment created. "
                "Confirm via POST /api/payments/bkash/webhook/"
            ),
            "raw_response": {
                "paymentID": transaction_id,
                "status": "Initiated",
                "amount": float(amount),
                "mode": "sandbox-mock",
            }
        }
