from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET

from rest_framework import generics
from rest_framework.permissions import AllowAny

from blog.models import Profile
from blog.serializers import ProfileSerializer


@method_decorator(require_GET, name="get")
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs.get("username")
        profile = get_object_or_404(Profile, user__username=username)

        return profile
