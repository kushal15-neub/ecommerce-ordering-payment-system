# Import DRF generic views
from rest_framework import generics

# Import APIView and Response
from rest_framework.views import APIView
from rest_framework.response import Response

# Import models
from .models import Product, Category

# Import serializer
from .serializers import ProductSerializer

# Import services
from .services import (
    get_category_tree,
    get_category_and_children_ids
)


# ==================================================
# Product List + Create API
# ==================================================
class ProductListCreateView(generics.ListCreateAPIView):

    serializer_class = ProductSerializer

    def get_queryset(self):

        queryset = Product.objects.all()

        category_id = self.request.query_params.get(
            'category'
        )

        if category_id:

            try:

                category = Category.objects.get(
                    id=category_id
                )

                category_ids = (
                    get_category_and_children_ids(
                        category
                    )
                )

                queryset = queryset.filter(
                    category_id__in=category_ids
                )

            except Category.DoesNotExist:

                return Product.objects.none()

        return queryset


# ==================================================
# Product Detail API
# ==================================================
class ProductDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer


# ==================================================
# Category Tree API
# ==================================================
class CategoryTreeAPIView(APIView):

    def get(self, request, category_id):

        data = get_category_tree(
            category_id
        )

        return Response({
            "category_id": category_id,
            "children": data
        })