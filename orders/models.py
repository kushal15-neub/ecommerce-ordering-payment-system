# Import Django models
from django.db import models

# Import custom user model
from users.models import User

# Import Product model
from products.models import Product


class Order(models.Model):
    """
    Order model
    Stores customer orders
    """

    # Customer who places order
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # Product ordered
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    # Quantity ordered
    quantity = models.PositiveIntegerField()

    # Order creation time
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id}"