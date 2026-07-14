# Import Django URL tools
from django.urls import path

# Import views
from .views import (
    OrderListCreateView,
    OrderDetailView
)

# URL patterns
urlpatterns = [

    # List all orders for logged-in user
    # Create new order
    path(
        '',
        OrderListCreateView.as_view(),
        name='order-list-create'
    ),

    # Retrieve, update, delete specific order
    path(
        '<int:pk>/',
        OrderDetailView.as_view(),
        name='order-detail'
    ),
]