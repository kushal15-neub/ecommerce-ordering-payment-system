from django.core.management.base import BaseCommand

from users.models import User
from products.models import Category, Product


class Command(BaseCommand):

    help = "Seed sample data"

    def handle(self, *args, **kwargs):

        # Admin User

        if not User.objects.filter(
            username="admin"
        ).exists():

            User.objects.create_user(
                username="admin",
                email="admin@gmail.com",
                password="Admin123!",
                role="admin",
                is_staff=True,
                is_superuser=True
            )

        electronics, _ = Category.objects.get_or_create(
            name="Electronics"
        )

        Product.objects.get_or_create(
            name="Laptop",
            defaults={
                "sku": "LAP-001",
                "description": "High performance laptop",
                "category": electronics,
                "price": 50000,
                "stock": 20
            }
        )

        Product.objects.get_or_create(
            name="Mouse",
            defaults={
                "sku": "MOU-001",
                "description": "Wireless optical mouse",
                "category": electronics,
                "price": 800,
                "stock": 100
            }
        )

        Product.objects.get_or_create(
            name="Keyboard",
            defaults={
                "sku": "KEY-001",
                "description": "Mechanical gaming keyboard",
                "category": electronics,
                "price": 1500,
                "stock": 50
            }
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Seed data created successfully."
            )
        )
