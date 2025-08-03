from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_http_methods

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from blog.models import Profile
from blog.serializers import ProfileSerializer


@method_decorator(require_GET, name="get")
@method_decorator(require_http_methods(["PUT"]), name="put")
@method_decorator(require_http_methods(["PATCH"]), name="patch")
class DashboardProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def update(self, request, *args, **kwargs):
        profile = self.get_queryset()
        partial = request.method == "PATCH"
        serializer = ProfileSerializer(profile, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save(user=self.request.user)

            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
