from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from blog.models import Post, Notification, Comment
from blog.serializers import CommentSerializer


@method_decorator(require_POST, name="post")
class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request):
        body = request.data.get("body", None)
        post = get_object_or_404(Post, id=request.data.get("post_id", None))
        comment = CommentSerializer(data={"post": post.id, "body": body})

        if comment.is_valid():
            comment.save(user=request.user)
            Notification.objects.create(user=request.user, post=post, type="comment")

            return JsonResponse(comment.data, status=201)
        else:
            return JsonResponse(comment.errors, status=400)


@method_decorator(require_GET, name="get")
class DashboardCommentListsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post__user=self.request.user)


@method_decorator(require_GET, name="get")
@method_decorator(require_http_methods(["DELETE"]), name="delete")
class DashboardCommentsRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comment_id = self.kwargs.get("id")

        return get_object_or_404(Comment, user=self.request.user, id=comment_id)

    def get_object(self):
        comment_id = self.kwargs.get("id")

        return get_object_or_404(Comment, user=self.request.user, id=comment_id)
