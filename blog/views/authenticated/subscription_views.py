from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from blog.models import Subscription
from blog.serializers import SubscriptionSerializer


@method_decorator(require_GET, name="get")
class DashboardSubscriptionListsAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(
            user=self.request.user, active=True
        ).order_by("-id")
