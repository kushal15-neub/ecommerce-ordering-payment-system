from django.urls import path

from .views import (
    ProductListCreateView,
    ProductDetailView,
    CategoryTreeAPIView,
)

urlpatterns = [

    # GET all products
    # POST create product
    path(
        '',
        ProductListCreateView.as_view(),
        name='product-list-create'
    ),

    # GET one product
    # PUT update product
    # DELETE product
    path(
        '<int:pk>/',
        ProductDetailView.as_view(),
        name='product-detail'
    ),

    # DFS Category Tree API
    path(
        'categories/<int:category_id>/tree/',
        CategoryTreeAPIView.as_view(),
        name='category-tree'
    ),

]