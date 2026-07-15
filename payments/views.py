from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

import json
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

stripe.api_key = settings.STRIPE_SECRET_KEY


# --------------------------------------------------
# Payment List
# --------------------------------------------------
class PaymentListView(ListAPIView):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# --------------------------------------------------
# Payment Detail
# --------------------------------------------------
class PaymentDetailView(RetrieveAPIView):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# --------------------------------------------------
# Create Payment
# --------------------------------------------------
class CreatePaymentView(APIView):

    def post(self, request):

        order_id = request.data.get("order")
        provider = request.data.get("provider")

        try:
            order = Order.objects.get(id=order_id)

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

        # Stripe starts as pending

        payment_status = "pending"

        if result["provider"] == "bkash":
            payment_status = result["status"]

        payment = Payment.objects.create(
            order=order,
            provider=result["provider"],
            transaction_id=result["transaction_id"],
            status=payment_status,
            raw_response=result
        )

        # Mock bKash success handling

        if payment.status == "success":

            order.status = "paid"
            order.save()

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


# --------------------------------------------------
# Stripe Webhook
# --------------------------------------------------
@method_decorator(csrf_exempt, name='dispatch')
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

        except Exception as e:

            print("WEBHOOK ERROR:", e)

            return HttpResponse(status=400)

        print("EVENT RECEIVED:", event["type"])

        # --------------------------------------------------
        # Payment Success
        # --------------------------------------------------

        if event["type"] == "payment_intent.succeeded":

            payment_intent = event["data"]["object"]

            transaction_id = payment_intent["id"]

            print("WEBHOOK RECEIVED:", transaction_id)

            try:

                payment = Payment.objects.get(
                    transaction_id=transaction_id
                )

                print("PAYMENT FOUND")

                payment.status = "success"
                payment.save()

                order = payment.order

                order.status = "paid"
                order.save()

                order_items = OrderItem.objects.filter(
                    order=order
                )

                for item in order_items:

                    product = item.product

                    product.stock -= item.quantity

                    product.save()

                print(
                    f"ORDER {order.id} MARKED AS PAID"
                )

            except Payment.DoesNotExist:

                print(
                    "PAYMENT NOT FOUND:",
                    transaction_id
                )

        # --------------------------------------------------
        # Payment Failed
        # --------------------------------------------------

        elif event["type"] == "payment_intent.payment_failed":

            payment_intent = event["data"]["object"]

            transaction_id = payment_intent["id"]

            print(
                "PAYMENT FAILED EVENT:",
                transaction_id
            )

            try:

                payment = Payment.objects.get(
                    transaction_id=transaction_id
                )

                payment.status = "failed"
                payment.save()

                print(
                    f"PAYMENT {payment.id} MARKED FAILED"
                )

            except Payment.DoesNotExist:

                print(
                    "PAYMENT NOT FOUND:",
                    transaction_id
                )

        return HttpResponse(status=200)