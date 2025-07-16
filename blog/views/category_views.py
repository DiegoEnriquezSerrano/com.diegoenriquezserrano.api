from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Category
from blog.serializers import CategorySerializer, PostSerializer


@method_decorator(require_GET, name="get")
@method_decorator(require_POST, name="post")
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        return Category.objects.all()

    def post(self, request):
        data = {"name": self.request.data.get("name")}
        category = CategorySerializer(data=data)

        if category.is_valid():
            category.save(user=self.request.user)

            return JsonResponse(category.data, status=201)
        else:
            return JsonResponse(category.errors, status=400)


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
