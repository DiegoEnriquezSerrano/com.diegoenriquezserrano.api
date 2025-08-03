from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Post
from blog.serializers import PostSerializer


@method_decorator(require_GET, name="get")
class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(draft=False)


@method_decorator(require_GET, name="get")
class PostRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        return Post.find_by_slug_and_username(
            self.kwargs["slug"], self.kwargs["username"]
        )


@method_decorator(require_GET, name="get")
class PostListByUserAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.find_list_by_username(self.kwargs["username"])
