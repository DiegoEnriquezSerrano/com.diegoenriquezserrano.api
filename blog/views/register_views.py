from django.http import JsonResponse

from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from blog.models import User
from blog.serializers import RegisterSerializer, ChallengeImageSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        challenge = ChallengeImageSerializer(data={**request.data})

        if not challenge.is_valid():
            return JsonResponse(
                {"captcha": ["Invalid captcha"]},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
