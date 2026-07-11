# Import APIView class from DRF
from rest_framework.views import APIView

# Import Response object for sending JSON
from rest_framework.response import Response

# Import Product model
from .models import Product

# Import Product serializer
from .serializers import ProductSerializer


# API endpoint for listing products
class ProductListView(APIView):

    def get(self, request):

        # Get all products from database
        products = Product.objects.all()

        # Convert products into JSON format
        serializer = ProductSerializer(
            products,
            many=True
        )

        # Return JSON response
        return Response(serializer.data)