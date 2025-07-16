from rest_framework import generics, status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from blog.models import User
from blog.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
