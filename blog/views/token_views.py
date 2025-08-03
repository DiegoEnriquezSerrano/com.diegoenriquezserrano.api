from django.http import JsonResponse
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
            key="access_token",
            value=serializer.validated_data["access"],
            httponly=True,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=serializer.validated_data["refresh"],
            httponly=True,
            samesite="Lax",
        )
        return response
