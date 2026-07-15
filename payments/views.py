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
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)
class PaymentListView(ListAPIView):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailView(RetrieveAPIView):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

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

        # Prevent duplicate payment

        if order.status == "paid":

            return Response(
                {
                    "error": "Order already paid"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check stock before payment

        order_items = OrderItem.objects.filter(
            order=order
        )

        for item in order_items:

            if item.product.stock < item.quantity:

                return Response(
                    {
                        "error": f"Insufficient stock for {item.product.name}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
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

        # Successful Payment

        if payment.status == "success":

            order.status = "paid"
            order.save()

            # Reduce stock

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
        