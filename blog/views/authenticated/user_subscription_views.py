from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.db.models import Q

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from blog.models import UserSubscription, User
from blog.serializers import (
    UserSubscriptionSerializer,
    CreateUserSubscriptionSerializer,
)


@method_decorator(require_GET, name="get")
class DashboardUserSubscriptionListsAPIView(generics.ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSubscription.objects.filter(
            user=self.request.user, active=True
        ).order_by("-id")


@method_decorator(require_POST, name="post")
class DashboardUserSubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        create_serializer = CreateUserSubscriptionSerializer(
            data={"user": user.id, "subscriber": self.request.user.id}
        )

        if create_serializer.is_valid():
            user_subscription = create_serializer.save()
            serializer = UserSubscriptionSerializer(instance=user_subscription)

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(
                create_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


@method_decorator(require_GET, name="get")
@method_decorator(require_http_methods(["PUT"]), name="put")
class DashboardUserSubscriptionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            UserSubscription,
            Q(user__id=self.request.user.id) | Q(subscriber__id=self.request.user.id),
            id=self.kwargs["id"],
        )

    def get_queryset(self):
        return get_object_or_404(
            UserSubscription,
            Q(user__id=self.request.user.id) | Q(subscriber__id=self.request.user.id),
            id=self.kwargs["id"],
        )

    def put(self, request, *args, **kwargs):
        user_subscription = self.get_queryset()
        partial = request.method == "PATCH"
        update_serializer = CreateUserSubscriptionSerializer(
            user_subscription,
            data={
                "active": request.data.get("active", None),
                "user": user_subscription.user.id,
                "subscriber": user_subscription.subscriber.id,
            },
            partial=partial,
        )

        if update_serializer.is_valid():
            user_subscription = update_serializer.save()
            serializer = UserSubscriptionSerializer(instance=user_subscription)

            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(
                update_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
