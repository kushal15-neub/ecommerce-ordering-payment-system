# Import DRF generic views
from rest_framework import generics

# Import Product model
from .models import Product

# Import Product serializer
from .serializers import ProductSerializer


# ---------------------------------------------------
# Product List + Create API
# ---------------------------------------------------
class ProductListCreateView(generics.ListCreateAPIView):

    # Fetch all products
    queryset = Product.objects.all()

    # Convert model <-> JSON
    serializer_class = ProductSerializer


# ---------------------------------------------------
# Product Detail + Update + Delete API
# ---------------------------------------------------
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    # Fetch all products
    queryset = Product.objects.all()

    # Convert model <-> JSON
    serializer_class = ProductSerializer