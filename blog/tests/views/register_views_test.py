import json
import os

from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from blog.models.user import User
from blog.tests.factories import UserFactory


class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
            "password2": "testpassword",
        }

    @mock.patch(
        "blog.services.EmailService.perform_send", return_value={"Message": "OK"}
    )
    def test_user_registration_success(self, mock_postmark_client):
        response = self.client.post("/user/register", self.data)
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(mock_postmark_client.called, True)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())
        self.assertEqual(
            response_json,
            {"username": self.data["username"], "email": self.data["email"]},
        )

    @mock.patch(
        "blog.services.EmailService.perform_send", return_value={"Message": "OK"}
    )
    def test_user_registration_email_call_args(self, mock_postmark_client):
        self.client.post("/user/register", self.data)
        self.assertEqual(mock_postmark_client.called, True)

        args = mock_postmark_client.call_args

        self.assertEqual(args[0][0]["from"], os.getenv("DEFAULT_FROM_EMAIL"))
        self.assertEqual(args[0][0]["to"], self.data["email"])
        self.assertEqual(args[0][0]["subject"], "User confirmation required")

    @mock.patch(
        "blog.services.EmailService.perform_send", return_value={"Message": "OK"}
    )
    def test_user_registration_email_html_body(self, mock_postmark_client):
        self.client.post("/user/register", self.data)
        self.assertEqual(mock_postmark_client.called, True)

        args = mock_postmark_client.call_args[0][0]["html_body"]

        self.assertIn(f"Welcome {self.data['username']}", args)
        self.assertIn(
            "Click the button below to verify your email and complete your account setup:",
            args,
        )
        self.assertIn(
            f"{os.getenv('CORS_ALLOWED_ORIGIN_CLIENT')}/user/confirmation/", args
        )

    @mock.patch(
        "blog.services.EmailService.perform_send", return_value={"Message": "OK"}
    )
    def test_user_registration_email_text_body(self, mock_postmark_client):
        self.client.post("/user/register", self.data)
        self.assertEqual(mock_postmark_client.called, True)

        args = mock_postmark_client.call_args[0][0]["text_body"]

        self.assertIn(f"Hello {self.data['username']},", args)
        self.assertIn(
            "Your account requires confirmation, to complete this step copy and paste the following URL into your browser address bar:",
            args,
        )
        self.assertIn(
            f"{os.getenv('CORS_ALLOWED_ORIGIN_CLIENT')}/user/confirmation/",
            args,
        )

    def test_user_registration_duplicate_email(self):
        UserFactory(email="testuser@example.com", username="testuser")
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
        UserFactory(email="testuser@example.com", username="testuser")
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
