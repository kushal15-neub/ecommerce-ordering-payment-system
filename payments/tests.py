from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User
from products.models import Category, Product
from orders.models import Order, OrderItem
from payments.models import Payment
from payments.strategies import BkashPaymentStrategy


class PaymentTests(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.user = User.objects.create_user(
            username="buyer",
            email="buyer@test.com",
            password="Pass1234!",
            role=User.CUSTOMER
        )

        category = Category.objects.create(name="Electronics")

        self.product = Product.objects.create(
            name="Mouse",
            sku="MOU-001",
            description="Test mouse",
            price=500,
            stock=10,
            category=category
        )

        self.order = Order.objects.create(
            user=self.user,
            total_amount=500,
            status="pending"
        )

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=500,
            subtotal=500
        )

    def test_bkash_strategy_returns_pending(self):

        strategy = BkashPaymentStrategy()
        result = strategy.pay(500)

        self.assertEqual(result["provider"], "bkash")
        self.assertEqual(result["status"], "pending")
        self.assertTrue(
            result["transaction_id"].startswith("BKASH-")
        )

    def test_bkash_webhook_marks_order_paid(self):

        payment = Payment.objects.create(
            order=self.order,
            provider="bkash",
            transaction_id="BKASH-TEST123",
            status="pending",
            raw_response={}
        )

        response = self.client.post(
            "/api/payments/bkash/webhook/",
            {
                "transaction_id": "BKASH-TEST123",
                "status": "success"
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        payment.refresh_from_db()
        self.order.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(payment.status, "success")
        self.assertEqual(self.order.status, "paid")
        self.assertEqual(self.product.stock, 9)
