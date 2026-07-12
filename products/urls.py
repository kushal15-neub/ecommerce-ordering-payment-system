from django.urls import path
from .views import ProductListCreateView, ProductDetailView

from .views import (
    ProductListCreateView,
    ProductDetailView
)

urlpatterns = [

    # GET, POST
    path(
        '',
        ProductListCreateView.as_view(),
        name='product-list-create'
    ),

    # GET ONE, PUT, DELETE
    path(
        '<int:pk>/',
        ProductDetailView.as_view(),
        name='product-detail'
    ),

]

urlpatterns = [

    path(
        '',
        ProductListCreateView.as_view(),
        name='product-list-create'
    ),

    path(
        '<int:pk>/',
        ProductDetailView.as_view(),
        name='product-detail'
    ),

]