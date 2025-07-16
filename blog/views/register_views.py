from rest_framework import generics

from rest_framework.permissions import AllowAny

from blog.models import User
from blog.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
