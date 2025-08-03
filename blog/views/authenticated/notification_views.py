from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_http_methods

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from blog.models import Notification
from blog.serializers import NotificationSerializer


@method_decorator(require_GET, name="get")
class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(read=False, post__user=self.request.user)


@method_decorator(require_http_methods(["PUT"]), name="put")
@method_decorator(require_http_methods(["PATCH"]), name="patch")
class NotificationUpdateAPIView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Notification,
            id=self.kwargs["notification_id"],
            post__user=self.request.user,
            read=False,
        )

    def get_queryset(self):
        return get_object_or_404(
            Notification,
            id=self.kwargs["notification_id"],
            read=False,
            post__user=self.request.user,
        )

    def update(self, request, *args, **kwargs):
        notification = self.get_queryset()
        notification.read = True
        notification.full_clean()
        notification.save()

        return JsonResponse({"message": "notification read"}, status=status.HTTP_200_OK)
