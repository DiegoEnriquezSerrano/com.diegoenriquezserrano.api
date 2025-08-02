from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Category
from blog.serializers import CategorySerializer, PostSerializer


@method_decorator(require_GET, name="get")
class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        return Category.objects.all()


@method_decorator(require_GET, name="get")
class CategoryRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return Category.find_by_slug_and_username(
            self.kwargs["slug"], self.kwargs["username"]
        )


@method_decorator(require_GET, name="get")
class CategoryListByUserAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Category.find_list_by_username(self.kwargs["username"])


@method_decorator(require_GET, name="get")
class CategoryPostsListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Category.find_by_slug_and_username(
            self.kwargs["slug"], self.kwargs["username"]
        ).posts.filter(draft=False)
