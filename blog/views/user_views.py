from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from blog.models import Profile, User
from blog.serializers import ProfileSerializer


@method_decorator(require_GET, name="get")
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs.get("username")
        profile = Profile.objects.get(user__username=username)

        return profile
