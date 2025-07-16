from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_http_methods

from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from blog.models import Category
from blog.serializers import CategorySerializer


@method_decorator(require_GET, name="get")
class DashboardCategoryListsAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by("-id")


@method_decorator(require_GET, name="get")
@method_decorator(require_http_methods(["PUT"]), name="put")
@method_decorator(require_http_methods(["PATCH"]), name="patch")
@method_decorator(require_http_methods(["DELETE"]), name="delete")
class DashboardCategoriesRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs.get("slug")

        return get_object_or_404(Category, user=self.request.user, slug=slug)

    def get_object(self):
        slug = self.kwargs.get("slug")

        return get_object_or_404(Category, user=self.request.user, slug=slug)

    def update(self, request, *args, **kwargs):
        category = self.get_queryset()
        partial = request.method == "PATCH"
        serializer = CategorySerializer(category, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save(user=self.request.user)

            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
