from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from blog.models import Post, Notification, Category
from blog.serializers import PostSerializer, CreatePostSerializer


@method_decorator(require_GET, name="get")
@method_decorator(require_POST, name="post")
class DashboardPostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user, draft=False).order_by("-id")

    def post(self, request):
        serializer = CreatePostSerializer(
            data={**request.data, "user": self.request.user.id}
        )

        if serializer.is_valid():
            result = serializer.save()

            return JsonResponse(PostSerializer(result).data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


@method_decorator(require_GET, name="get")
class DashboardPostDraftListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user, draft=True).order_by("-id")


@method_decorator(require_GET, name="get")
class DashboardCategoryPostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")

        return Category.find_by_slug_and_username(
            category_slug, self.request.user.username
        ).posts.filter(draft=False)


@method_decorator(require_GET, name="get")
@method_decorator(require_http_methods(["PUT"]), name="put")
@method_decorator(require_http_methods(["PATCH"]), name="patch")
@method_decorator(require_http_methods(["DELETE"]), name="delete")
class DashboardPostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs["slug"])

    def get_queryset(self):
        return get_object_or_404(Post, slug=self.kwargs["slug"], user=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_queryset()
        partial = request.method == "PATCH"
        serializer = CreatePostSerializer(
            post,
            data={
                **request.data,
                "user": self.request.user.id,
                "last_modified": datetime.utcnow(),
            },
            partial=partial,
        )

        if serializer.is_valid():
            result = serializer.save()

            return JsonResponse(PostSerializer(result).data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(require_POST, name="post")
class PostLikeCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = find_post(request).toggle_like(request.user)

        if result == "liked":
            post = find_post(request)
            Notification.objects.create(user=request.user, post=post, type="like")

            return JsonResponse({"message": result}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"message": result}, status=status.HTTP_200_OK)


def find_post(request):
    post_id = request.data.get("post_id", None)

    return get_object_or_404(Post, id=post_id)
