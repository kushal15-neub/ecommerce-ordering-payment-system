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
    get_category_and_children_ids,
    get_recommended_products
)

# Import permissions
from .permissions import IsAdminUserRole


# ==================================================
# Product List + Create API
# ==================================================
class ProductListCreateView(
    generics.ListCreateAPIView
):

    serializer_class = ProductSerializer
    permission_classes = [IsAdminUserRole]

    def get_queryset(self):

        queryset = Product.objects.all()

        category_id = self.request.query_params.get(
            "category"
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
    permission_classes = [IsAdminUserRole]


# ==================================================
# Category Tree API
# ==================================================
class CategoryTreeAPIView(APIView):

    def get(self, request, category_id):

        data = get_category_tree(
            category_id
        )

        return Response(
            {
                "category_id": category_id,
                "children": data
            }
        )


# ==================================================
# Product Recommendations API (DFS)
# ==================================================
class ProductRecommendationsAPIView(APIView):

    def get(self, request, pk):

        try:
            product = Product.objects.get(pk=pk)

        except Product.DoesNotExist:

            return Response(
                {"error": "Product not found"},
                status=404
            )

        recommendations = get_recommended_products(product)

        serializer = ProductSerializer(
            recommendations,
            many=True
        )

        return Response(
            {
                "product_id": pk,
                "recommendations": serializer.data
            }
        )