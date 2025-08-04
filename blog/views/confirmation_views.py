from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from blog.models import User
from blog.services.confirmation_service import ConfirmationService


@method_decorator(require_http_methods(["PUT"]), name="put")
@method_decorator(require_http_methods(["PATCH"]), name="patch")
class ConfirmationView(generics.UpdateAPIView):
    permission_classes = [AllowAny]

    def get_object(self):
        url_decoded_token = self.kwargs["signed_confirmation_token"].replace("%3A", ":")
        unsigned_token = ConfirmationService.attempt_token_unsign(url_decoded_token)

        return get_object_or_404(
            User,
            confirmation_token=unsigned_token,
        )

    def get_queryset(self):
        url_decoded_token = self.kwargs["signed_confirmation_token"].replace("%3A", ":")
        unsigned_token = ConfirmationService.attempt_token_unsign(url_decoded_token)

        return get_object_or_404(
            User,
            confirmation_token=unsigned_token,
        )

    def update(self, request, *args, **kwargs):
        user = self.get_queryset()

        if not user.confirmed:
            user.attempt_confirmation()

            return JsonResponse(
                {"message": "user confirmation OK"}, status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {"confirmation_token": ["token is invalid"]},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
