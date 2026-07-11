# Import path function for URL routing
from django.urls import path

# Import our Product API View
from .views import ProductListView


urlpatterns = [

    # GET /api/products/
    path(
        '',
        ProductListView.as_view(),
        name='product-list'
    ),

]