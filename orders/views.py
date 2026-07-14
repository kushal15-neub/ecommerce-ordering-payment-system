from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer


# -------------------------------------
# List My Orders + Create Order
# -------------------------------------
class OrderListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


# -------------------------------------
# Order Detail
# -------------------------------------
class OrderDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.user
        )