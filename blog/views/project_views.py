from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET

from rest_framework import generics
from rest_framework.permissions import AllowAny

from blog.models import Project
from blog.serializers import ProjectSerializer


@method_decorator(require_GET, name="get")
class ProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Project.objects.all()


@method_decorator(require_GET, name="get")
class ProjectRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Project.find_by_slug_and_username(
            self.kwargs["slug"], self.kwargs["username"]
        )


@method_decorator(require_GET, name="get")
class ProjectListByUsernameAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Project.find_list_by_username(self.kwargs["username"])
