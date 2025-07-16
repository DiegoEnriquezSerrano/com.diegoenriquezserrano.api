from django.db.models import Sum, Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from blog.models import Post, Bookmark
from blog.serializers import AuthorSerializer


@method_decorator(require_GET, name="get")
class AuthorStatsAPIView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(user=user).count()
        likes = (
            (
                Post.objects.filter(user=user)
                .annotate(Count("likes"))
                .aggregate(Sum("likes__count"))["likes__count__sum"]
            )
            or 0
        )
        bookmarks = Bookmark.objects.filter(user=user).count()

        return [{"posts": posts, "bookmarks": bookmarks, "likes": likes}]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return JsonResponse(serializer.data[0])
