from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_http_methods

from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from blog.models import Subscription, User
from blog.services.confirmation_service import ConfirmationService
from blog.serializers import (
    SubscriptionSerializer,
    ChallengeImageSerializer,
    CreateSubscriptionSerializer,
)


@method_decorator(require_POST, name="post")
class SubscriptionCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        challenge = ChallengeImageSerializer(data=request.data)

        if not challenge.is_valid():
            return JsonResponse(
                {"captcha": ["Invalid captcha"]},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user = get_object_or_404(User, username=self.kwargs.get("username"))
        serializer = CreateSubscriptionSerializer(
            data={**request.data, "user": user.id}
        )

        if serializer.is_valid():
            result = serializer.save()

            return JsonResponse(
                SubscriptionSerializer(result).data, status=status.HTTP_201_CREATED
            )

        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(require_http_methods(["PUT"]), name="put")
@method_decorator(require_http_methods(["PATCH"]), name="patch")
class SubscriptionConfirmationUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]

    def get_object(self):
        url_decoded_token = self.kwargs["signed_confirmation_token"].replace("%3A", ":")
        unsigned_token = ConfirmationService.attempt_token_unsign(url_decoded_token)

        return get_object_or_404(
            Subscription,
            confirmation_token=unsigned_token,
        )

    def get_queryset(self):
        url_decoded_token = self.kwargs["signed_confirmation_token"].replace("%3A", ":")
        unsigned_token = ConfirmationService.attempt_token_unsign(url_decoded_token)

        return get_object_or_404(
            Subscription,
            confirmation_token=unsigned_token,
        )

    def update(self, request, *args, **kwargs):
        subscription = self.get_queryset()

        if not subscription.confirmed:
            subscription.attempt_confirmation()

            return JsonResponse(
                {"message": "subscription confirmation OK"}, status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {"confirmation_token": ["token is invalid"]},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
