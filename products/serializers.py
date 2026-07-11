# Import DRF serializer tools
from rest_framework import serializers

# Import Product model
from .models import Product


# Serializer converts Product objects into JSON
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = '__all__'