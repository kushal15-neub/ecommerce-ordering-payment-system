from django.test import TestCase

from users.models import User
from products.models import Category, Product
from orders.models import Order, OrderItem


class OrderModelTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="buyer",
            email="buyer@test.com",
            password="Pass1234!",
            role=User.CUSTOMER
        )

        category = Category.objects.create(name="Electronics")

        self.product = Product.objects.create(
            name="Laptop",
            sku="LAP-001",
            description="Test laptop",
            price=1000,
            stock=5,
            category=category
        )

    def test_order_total_calculation(self):

        order = Order.objects.create(
            user=self.user,
            status="pending"
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price=1000
        )

        order.total_amount = 2000
        order.save()

        self.assertEqual(order.total_amount, 2000)
        self.assertEqual(order.items.count(), 1)
