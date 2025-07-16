from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from blog.models import Post, Notification
from blog.serializers import PostSerializer


@method_decorator(require_GET, name="get")
class DashboardPostListsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user, draft=False).order_by("-id")


@method_decorator(require_GET, name="get")
@method_decorator(require_http_methods(["PUT"]), name="put")
@method_decorator(require_http_methods(["PATCH"]), name="patch")
@method_decorator(require_http_methods(["DELETE"]), name="delete")
class DashboardPostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Post.objects.get(id=self.kwargs["post_id"])

    def get_queryset(self):
        return Post.objects.get(id=self.kwargs["post_id"], user=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_queryset()
        partial = request.method == "PATCH"
        serializer = PostSerializer(post, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
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
