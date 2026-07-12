from rest_framework import generics

from .models import Order
from .serializers import OrderSerializer


# List Orders + Create Order
class OrderListCreateView(generics.ListCreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# Retrieve + Update + Delete
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer