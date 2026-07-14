from django.urls import path

from .views import CreatePaymentView

urlpatterns = [

    path(
        '',
        CreatePaymentView.as_view(),
        name='payment-create'
    ),

]