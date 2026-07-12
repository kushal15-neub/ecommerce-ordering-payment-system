# Import DRF serializer tools
from rest_framework import serializers

# Import Product model
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Converts Product objects to JSON
    and JSON data to Product objects
    """

    class Meta:
        model = Product
        fields = "__all__"