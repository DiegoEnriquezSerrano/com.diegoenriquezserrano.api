from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from blog.models import Project
from blog.serializers import ProjectSerializer, CreateProjectSerializer


@method_decorator(require_GET, name="get")
@method_decorator(require_POST, name="post")
class DashboardProjectListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(user=self.request.user)

    def post(self, request):
        data = {**self.request.data, "user": self.request.user.id}
        serializer = CreateProjectSerializer(data=data)

        if serializer.is_valid():
            record = serializer.save(user=self.request.user)
            project = ProjectSerializer(record)

            return JsonResponse(project.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


@method_decorator(require_GET, name="get")
@method_decorator(require_http_methods(["PUT"]), name="put")
@method_decorator(require_http_methods(["PATCH"]), name="patch")
@method_decorator(require_http_methods(["DELETE"]), name="delete")
class DashboardProjectRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs.get("slug")

        return get_object_or_404(Project, user=self.request.user, slug=slug)

    def get_object(self):
        slug = self.kwargs.get("slug")

        return get_object_or_404(Project, user=self.request.user, slug=slug)

    def update(self, request, *args, **kwargs):
        record = self.get_queryset()
        partial = request.method == "PATCH"
        data = {**request.data, "user": self.request.user.id}
        serializer = CreateProjectSerializer(record, data=data, partial=partial)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            project = ProjectSerializer(record)

            return JsonResponse(project.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
