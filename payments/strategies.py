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
            amount=int(float(amount) * 100),  # Stripe uses cents
            currency="usd",
            automatic_payment_methods={
                "enabled": True
            }
        )

        return {
    "provider": "stripe",
    "transaction_id": payment_intent.id,
    "client_secret": payment_intent.client_secret,
    "status": payment_intent.status,
    "amount": float(amount),
    "raw_response": {
        "id": payment_intent.id,
        "status": payment_intent.status,
        "client_secret": payment_intent.client_secret,
        "amount": payment_intent.amount,
        "currency": payment_intent.currency
    }
}

class BkashPaymentStrategy(PaymentStrategy):

    def pay(self, amount):

        return {
            "provider": "bkash",
            "transaction_id": str(uuid.uuid4()),
            "status": "pending",
            "amount": float(amount)
        }