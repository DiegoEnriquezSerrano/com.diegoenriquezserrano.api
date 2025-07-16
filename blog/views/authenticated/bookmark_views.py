from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_GET

from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from blog.models import Bookmark
from blog.serializers import BookmarkSerializer


@method_decorator(require_POST, name="post")
class BookmarkCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer

    def post(self, request):
        result = Bookmark.create_or_delete(
            request.user, request.data.get("post_id", None)
        )

        if result == "created":
            return JsonResponse(
                {"message": "bookmarked"}, status=status.HTTP_201_CREATED
            )
        else:
            return JsonResponse({"message": "unbookmarked"}, status=status.HTTP_200_OK)


@method_decorator(require_GET, name="get")
class DashboardBookmarkListsAPIView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).order_by("-id")
