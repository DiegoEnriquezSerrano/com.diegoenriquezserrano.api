import json
import os

from django.http import HttpResponse
from django.conf import settings
from django.core.signing import TimestampSigner

from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from blog.models.user import User
from blog.tests.factories import UserFactory
from blog.services.challenge_service import ChallengeService


ok_response = HttpResponse(status=status.HTTP_200_OK)


class UserRegistrationTests(APITestCase):
    def setUp(self):
        signer = TimestampSigner()
        self.challenge = ChallengeService.generate_image_challenge()
        self.challenge_answer = signer.unsign_object(self.challenge["signed_answer"])[
            "code"
        ]
        self.data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
            "password2": "testpassword",
            "challenge_answer": self.challenge_answer,
            "signed_answer": self.challenge["signed_answer"],
        }

    @mock.patch("blog.services.MailgunService.perform_send", return_value=ok_response)
    def test_user_registration_success(self, mock_postmark_client):
        response = self.client.post(
            "/user/register",
            self.data,
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(mock_postmark_client.called, True)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())
        self.assertEqual(
            response_json,
            {"username": self.data["username"], "email": self.data["email"]},
        )

    @mock.patch("blog.services.MailgunService.perform_send", return_value=ok_response)
    def test_user_registration_email_call_args(self, mock_postmark_client):
        self.client.post("/user/register", self.data)
        self.assertEqual(mock_postmark_client.called, True)

        args = mock_postmark_client.call_args

        self.assertEqual(args[0][0]["from"], settings.MAILGUN["FROM_EMAIL"])
        self.assertEqual(args[0][0]["to"], self.data["email"])
        self.assertEqual(args[0][0]["subject"], "User confirmation required")

    @mock.patch("blog.services.MailgunService.perform_send", return_value=ok_response)
    def test_user_registration_email_html_body(self, mock_postmark_client):
        self.client.post("/user/register", self.data)
        self.assertEqual(mock_postmark_client.called, True)

        args = mock_postmark_client.call_args[0][0]["html_body"]

        self.assertIn(f"{self.data['username']}", args)
        self.assertIn(
            "Click the button below to verify your email",
            args,
        )
        self.assertIn(
            f"{os.getenv('CORS_ALLOWED_ORIGIN_CLIENT')}/user/confirmation/", args
        )

    @mock.patch("blog.services.MailgunService.perform_send", return_value=ok_response)
    def test_user_registration_email_text_body(self, mock_postmark_client):
        self.client.post("/user/register", self.data)
        self.assertEqual(mock_postmark_client.called, True)

        args = mock_postmark_client.call_args[0][0]["text_body"]

        self.assertIn(f"{self.data['username']},", args)
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
            "challenge_answer": self.challenge_answer,
            "signed_answer": self.challenge["signed_answer"],
        }
        response = self.client.post("/user/register", data)
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response_json)

    def test_user_registration_duplicate_username(self):
        UserFactory(email="testuser@example.com", username="testuser")
        data = {
            "email": "newuser@example.com",
            "username": "testuser",
            "password": "newpassword",
            "password2": "newpassword",
            "challenge_answer": self.challenge_answer,
            "signed_answer": self.challenge["signed_answer"],
        }
        response = self.client.post("/user/register", data)
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response_json)

    def test_user_registration_missing_fields(self):
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "challenge_answer": self.challenge_answer,
            "signed_answer": self.challenge["signed_answer"],
        }
        response = self.client.post("/user/register", data)
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response_json)

    def test_user_registration_missing_second_password_fields(self):
        data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword",
            "challenge_answer": self.challenge_answer,
            "signed_answer": self.challenge["signed_answer"],
        }
        response = self.client.post("/user/register", data)
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password2", response_json)

    def test_user_registration_invalid_email(self):
        data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "testpassword",
            "password2": "testpassword",
            "challenge_answer": self.challenge_answer,
            "signed_answer": self.challenge["signed_answer"],
        }
        response = self.client.post("/user/register", data)
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response_json)
