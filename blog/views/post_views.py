import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Post
from blog.serializers import PostSerializer, UserSerializer


@method_decorator(require_GET, name="get")
@method_decorator(require_POST, name="post")
class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(draft=False)

    def post(self, request):
        post = PostSerializer(data=request.data)

        if post.is_valid():
            post.save(user=self.request.user)

            return JsonResponse(post.data, status=201)
        else:
            return JsonResponse(post.errors, status=400)


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
