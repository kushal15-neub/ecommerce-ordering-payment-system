from abc import ABC, abstractmethod
import uuid


class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, amount):
        pass


class StripePaymentStrategy(PaymentStrategy):

    def pay(self, amount):

        return {
            "provider": "stripe",
            "transaction_id": str(uuid.uuid4()),
            "status": "success",
            "amount": float(amount)
        }


class BkashPaymentStrategy(PaymentStrategy):

    def pay(self, amount):

        return {
            "provider": "bkash",
            "transaction_id": str(uuid.uuid4()),
            "status": "success",
            "amount": float(amount)      
}