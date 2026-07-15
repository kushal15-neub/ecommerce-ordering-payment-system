from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from orders.models import Order, OrderItem

from .models import Payment
from .serializers import PaymentSerializer
from .strategies import (
    StripePaymentStrategy,
    BkashPaymentStrategy
)
from .services import (
    complete_successful_payment,
    mark_payment_failed
)

import json
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentListView(ListAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            order__user=self.request.user
        )


class PaymentDetailView(RetrieveAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            order__user=self.request.user
        )


class CreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get("order")
        provider = request.data.get("provider")

        try:
            order = Order.objects.get(
                id=order_id,
                user=request.user
            )

        except Order.DoesNotExist:

            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if order.status == "paid":

            return Response(
                {"error": "Order already paid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_items = OrderItem.objects.filter(order=order)

        for item in order_items:

            if item.product.stock < item.quantity:

                return Response(
                    {
                        "error": (
                            f"Insufficient stock for "
                            f"{item.product.name}"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        if provider == "stripe":
            strategy = StripePaymentStrategy()

        elif provider == "bkash":
            strategy = BkashPaymentStrategy()

        else:

            return Response(
                {"error": "Invalid provider"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = strategy.pay(order.total_amount)

        payment = Payment.objects.create(
            order=order,
            provider=result["provider"],
            transaction_id=result["transaction_id"],
            status=result.get("status", "pending"),
            raw_response=result
        )

        serializer = PaymentSerializer(payment)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        payload = request.body

        try:
            event = stripe.Event.construct_from(
                json.loads(payload),
                stripe.api_key
            )

        except Exception:
            return HttpResponse(status=400)

        if event["type"] == "payment_intent.succeeded":

            payment_intent = event["data"]["object"]
            transaction_id = payment_intent["id"]

            try:
                payment = Payment.objects.get(
                    transaction_id=transaction_id
                )
                complete_successful_payment(payment)

            except Payment.DoesNotExist:
                pass

        elif event["type"] == "payment_intent.payment_failed":

            payment_intent = event["data"]["object"]
            transaction_id = payment_intent["id"]

            try:
                payment = Payment.objects.get(
                    transaction_id=transaction_id
                )
                mark_payment_failed(payment)

            except Payment.DoesNotExist:
                pass

        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name="dispatch")
class BkashWebhookView(APIView):
    """
    Mock bKash webhook simulating payment confirmation.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        transaction_id = request.data.get("transaction_id")
        payment_status = request.data.get("status", "success")

        if not transaction_id:

            return Response(
                {"error": "transaction_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = Payment.objects.get(
                transaction_id=transaction_id,
                provider="bkash"
            )

        except Payment.DoesNotExist:

            return Response(
                {"error": "Payment not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if payment_status == "success":
            complete_successful_payment(payment)

        elif payment_status == "failed":
            mark_payment_failed(payment)

        else:

            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.refresh_from_db()
        serializer = PaymentSerializer(payment)

        return Response(serializer.data)
