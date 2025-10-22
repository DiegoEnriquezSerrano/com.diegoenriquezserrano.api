from django.http import JsonResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from blog.serializers import BlogTokenObtainPairSerializer


@method_decorator(require_POST, name="post")
class BlogTokenObtainPairView(TokenObtainPairView):
    serializer_class = BlogTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = JsonResponse(
            {"message": "authentication ok"}, status=status.HTTP_200_OK
        )
        response.set_cookie(
            domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
            expires=None,
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            max_age=None,
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            value=serializer.validated_data["access"],
        )

        return response
