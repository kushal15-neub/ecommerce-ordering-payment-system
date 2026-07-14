from django.db import models

from orders.models import Order


class Payment(models.Model):

    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('bkash', 'Bkash')
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    provider = models.CharField(
        max_length=20,
        choices=PROVIDER_CHOICES
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    raw_response = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.provider} - {self.transaction_id}"