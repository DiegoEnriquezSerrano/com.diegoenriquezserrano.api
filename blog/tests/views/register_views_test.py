import json


from rest_framework import status
from rest_framework.test import APITestCase

from blog.models.user import User


class UserRegistrationTests(APITestCase):
    def test_user_registration_success(self):
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post("/user/register", data)
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json["username"], "testuser")
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_user_registration_duplicate_email(self):
        User.objects.create_user(
            email="testuser@example.com", username="testuser", password="testpassword"
        )
        data = {
            "email": "testuser@example.com",
            "username": "newuser",
            "password": "newpassword",
            "password2": "newpassword",
        }
        response = self.client.post("/user/register", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_user_registration_duplicate_username(self):
        User.objects.create_user(
            email="testuser@example.com", username="testuser", password="testpassword"
        )
        data = {
            "email": "newuser@example.com",
            "username": "testuser",
            "password": "newpassword",
            "password2": "newpassword",
        }
        response = self.client.post("/user/register", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_user_registration_missing_fields(self):
        data = {"email": "testuser@example.com", "username": "testuser"}
        response = self.client.post("/user/register", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_user_registration_missing_second_password_fields(self):
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post("/user/register", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password2", response.data)

    def test_user_registration_invalid_email(self):
        data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post("/user/register", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
