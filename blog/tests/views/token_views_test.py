import json

from rest_framework import status
from rest_framework.test import APITestCase

from blog.models.user import User


class BlogTokenObtainPairViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", username="testuser", password="testpassword"
        )

    def test_obtain_token_pair_success(self):
        response = self.client.post(
            "/user/token",
            {"email": "testuser@example.com", "password": "testpassword"},
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)
        self.assertEqual(response_json["message"], "authentication ok")

    def test_obtain_token_pair_invalid_credentials(self):
        response = self.client.post(
            "/user/token",
            {"email": "testuser@example.com", "password": "wrongpassword"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access_token", response.cookies)
        self.assertNotIn("refresh_token", response.cookies)

    def test_obtain_token_pair_missing_fields(self):
        response = self.client.post("/user/token", {"email": "testuser@example.com"})
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response_json)
        self.assertNotIn("access_token", response.cookies)
        self.assertNotIn("refresh_token", response.cookies)

    def test_obtain_token_pair_invalid_username(self):
        response = self.client.post(
            "/user/token",
            {"email": "invaliduser@example.com", "password": "testpassword"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access_token", response.cookies)
        self.assertNotIn("refresh_token", response.cookies)
