from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from blog.models import Subscription, User
from blog.serializers import SubscriptionSerializer


@method_decorator(require_POST, name="post")
class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        serializer = SubscriptionSerializer(
            data={"user": user.id, "email": request.data.get("email")}
        )

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
