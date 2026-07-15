from rest_framework import generics
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer


class RegisterView(
    generics.CreateAPIView
):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer