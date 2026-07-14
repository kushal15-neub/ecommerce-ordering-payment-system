from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order, OrderItem

from .models import Payment
from .serializers import PaymentSerializer

from .strategies import (
    StripePaymentStrategy,
    BkashPaymentStrategy
)


class CreatePaymentView(APIView):

    def post(self, request):

        order_id = request.data.get("order")
        provider = request.data.get("provider")

        try:
            order = Order.objects.get(
                id=order_id
            )

        except Order.DoesNotExist:

            return Response(
                {
                    "error": "Order not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Strategy Pattern

        if provider == "stripe":

            strategy = StripePaymentStrategy()

        elif provider == "bkash":

            strategy = BkashPaymentStrategy()

        else:

            return Response(
                {
                    "error": "Invalid provider"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = strategy.pay(
            order.total_amount
        )

        payment = Payment.objects.create(
            order=order,
            provider=result["provider"],
            transaction_id=result["transaction_id"],
            status=result["status"],
            raw_response=result
        )

        # Update Order Status

        if payment.status == "success":

            order.status = "paid"
            order.save()

            # Reduce Stock

            order_items = OrderItem.objects.filter(
                order=order
            )

            for item in order_items:

                product = item.product

                product.stock -= item.quantity

                product.save()

        serializer = PaymentSerializer(
            payment
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )