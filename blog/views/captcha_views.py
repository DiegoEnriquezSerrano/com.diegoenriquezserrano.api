from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_GET

from rest_framework import status

from blog.services.challenge_service import ChallengeService


@method_decorator(require_GET, name="get")
class ChallengeImageView(View):
    def get(self, request, *args, **kwargs):
        response = ChallengeService.generate_image_challenge()

        return JsonResponse(response, status=status.HTTP_200_OK)
