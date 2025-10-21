import json

from django.conf import settings
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from blog.models.user import User


class BlogTokenObtainPairViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="testpassword",
            confirmed=True,
            confirmed_at=timezone.now(),
        )

    def test_obtain_token_pair_success(self):
        response = self.client.post(
            "/user/token",
            {"email": "testuser@example.com", "password": "testpassword"},
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(settings.SIMPLE_JWT["AUTH_COOKIE"], response.cookies)
        self.assertEqual(response_json["message"], "authentication ok")

    def test_obtain_token_pair_invalid_credentials(self):
        response = self.client.post(
            "/user/token",
            {"email": "testuser@example.com", "password": "wrongpassword"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn(settings.SIMPLE_JWT["AUTH_COOKIE"], response.cookies)

    def test_obtain_token_pair_missing_fields(self):
        response = self.client.post("/user/token", {"email": "testuser@example.com"})
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response_json)
        self.assertNotIn(settings.SIMPLE_JWT["AUTH_COOKIE"], response.cookies)

    def test_obtain_token_pair_invalid_username(self):
        response = self.client.post(
            "/user/token",
            {"email": "invaliduser@example.com", "password": "testpassword"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn(settings.SIMPLE_JWT["AUTH_COOKIE"], response.cookies)
