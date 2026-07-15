from django.urls import path

from .views import (
    CreatePaymentView,
    PaymentListView,
    PaymentDetailView,
    StripeWebhookView,
    BkashWebhookView
)

urlpatterns = [
    path(
        '',
        PaymentListView.as_view(),
        name='payment-list'
    ),

    path(
        'create/',
        CreatePaymentView.as_view(),
        name='payment-create'
    ),

    path(
        '<int:pk>/',
        PaymentDetailView.as_view(),
        name='payment-detail'
    ),
    path(
        'stripe/webhook/',
        StripeWebhookView.as_view(),
        name='stripe-webhook'
    ),

    path(
        'bkash/webhook/',
        BkashWebhookView.as_view(),
        name='bkash-webhook'
    ),
]