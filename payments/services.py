from django.db import transaction

from orders.models import OrderItem


def complete_successful_payment(payment):
    """
    Mark payment and order as paid and reduce stock.
    Safe to call multiple times for the same order.
    """

    with transaction.atomic():

        order = payment.order

        if order.status == "paid":
            return

        payment.status = "success"
        payment.save(update_fields=["status", "updated_at"])

        order.status = "paid"
        order.save(update_fields=["status", "updated_at"])

        for item in OrderItem.objects.filter(order=order):

            product = item.product
            product.stock -= item.quantity
            product.save(update_fields=["stock"])


def mark_payment_failed(payment):

    payment.status = "failed"
    payment.save(update_fields=["status", "updated_at"])
