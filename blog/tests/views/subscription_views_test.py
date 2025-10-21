import json
import os
import urllib.parse

from django.conf import settings
from django.core.signing import TimestampSigner
from django.http import HttpResponse
from django.utils import timezone

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from unittest import mock

from blog.models import Subscription
from blog.services.challenge_service import ChallengeService
from blog.tests.factories import UserFactory, SubscriptionFactory

ok_response = HttpResponse(status=status.HTTP_200_OK)


class SubscriptionTests(APITestCase):
    def setUp(self):
        signer = TimestampSigner()
        subscription = SubscriptionFactory(email="subscriberexample@company.org")
        subscription.confirmed = False
        subscription.confirmed_at = None
        subscription.save()
        self.user = UserFactory(email="user@example.org")
        self.subscription = subscription
        self.signed_token = signer.sign_object(
            {"confirmation_token": self.subscription.confirmation_token}
        )
        self.challenge = ChallengeService.generate_image_challenge()
        self.challenge_answer = signer.unsign_object(self.challenge["signed_answer"])[
            "code"
        ]

    @mock.patch("blog.services.MailgunService.perform_send", return_value=ok_response)
    def test_unauthenticated_user_can_create_subscription(self, mock_mailgun_client):
        response = self.client.post(
            f"/subscribe/{self.user.username}",
            {
                "email": "newsubscriber@company.com",
                "challenge_answer": self.challenge_answer,
                "signed_answer": self.challenge["signed_answer"],
            },
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.filter(user=self.user).count(), 1)
        self.assertEqual(
            Subscription.objects.get(id=response_json["id"]).email,
            "newsubscriber@company.com",
        )
        self.assertEqual(mock_mailgun_client.called, True)

    @mock.patch("blog.services.MailgunService.perform_send", return_value=ok_response)
    def test_unauthenticated_user_cannot_create_with_invalid_captcha(
        self, mock_mailgun_client
    ):
        response = self.client.post(
            f"/subscribe/{self.user.username}",
            {
                "email": "newsubscriber@company.com",
                "challenge_answer": "wronganswer",
                "signed_answer": self.challenge["signed_answer"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(Subscription.objects.filter(user=self.user).count(), 0)
        self.assertEqual(mock_mailgun_client.called, False)

    @mock.patch("blog.services.MailgunService.perform_send", return_value=ok_response)
    def test_subscription_email_call_args(self, mock_mailgun_client):
        self.client.post(
            f"/subscribe/{self.user.username}",
            {
                "email": "newsubscriber@company.com",
                "challenge_answer": self.challenge_answer,
                "signed_answer": self.challenge["signed_answer"],
            },
        )
        self.assertEqual(mock_mailgun_client.called, True)

        args = mock_mailgun_client.call_args

        self.assertEqual(args[0][0]["from"], settings.MAILGUN["FROM_EMAIL"])
        self.assertEqual(args[0][0]["to"], "newsubscriber@company.com")
        self.assertEqual(args[0][0]["subject"], "Subscription confirmation required")

    @mock.patch("blog.services.MailgunService.perform_send", return_value=ok_response)
    def test_subscription_email_html_body(self, mock_mailgun_client):
        self.client.post(
            f"/subscribe/{self.user.username}",
            {
                "email": "newsubscriber@company.com",
                "challenge_answer": self.challenge_answer,
                "signed_answer": self.challenge["signed_answer"],
            },
        )
        self.assertEqual(mock_mailgun_client.called, True)

        args = mock_mailgun_client.call_args[0][0]["html_body"]

        self.assertIn("newsubscriber@company.com", args)
        self.assertIn(
            f"Click the button below to verify and complete your subscription to @{self.user.username}:",
            args,
        )
        self.assertIn(
            f"{os.getenv('CORS_ALLOWED_ORIGIN_CLIENT')}/subscription/confirmation/",
            args,
        )

    @mock.patch("blog.services.MailgunService.perform_send", return_value=ok_response)
    def test_subscription_email_text_body(self, mock_mailgun_client):
        self.client.post(
            f"/subscribe/{self.user.username}",
            {
                "email": "newsubscriber@company.com",
                "challenge_answer": self.challenge_answer,
                "signed_answer": self.challenge["signed_answer"],
            },
        )
        self.assertEqual(mock_mailgun_client.called, True)

        args = mock_mailgun_client.call_args[0][0]["text_body"]

        self.assertIn("Hello newsubscriber@company.com", args)
        self.assertIn(
            f"To complete your subscription to {self.user.username}, copy and paste the following URL into your browser address bar:",
            args,
        )
        self.assertIn(
            f"{os.getenv('CORS_ALLOWED_ORIGIN_CLIENT')}/subscription/confirmation/",
            args,
        )

    def test_cannot_create_duplicate_subscription(self):
        SubscriptionFactory(user=self.user, email="newsubscriber@company.com")

        response = self.client.post(
            f"/subscribe/{self.user.username}",
            {
                "email": "newsubscriber@company.com",
                "challenge_answer": self.challenge_answer,
                "signed_answer": self.challenge["signed_answer"],
            },
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["non_field_errors"][0],
            "The fields user, email must make a unique set.",
        )

    def test_unauthenticated_user_cannot_self_subscribe(self):
        response = self.client.post(
            f"/subscribe/{self.user.username}",
            {
                "email": self.user.email,
                "challenge_answer": self.challenge_answer,
                "signed_answer": self.challenge["signed_answer"],
            },
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["non_field_errors"][0],
            "Cannot self-subscribe",
        )

    def test_user_can_confirm_subscription_with_valid_token(self):
        response = self.client.put(
            f"/subscription/confirmation/{urllib.parse.quote(self.signed_token)}",
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.confirmed, True)
        self.assertEqual(response_json["message"], "subscription confirmation OK")

    def test_user_cannot_confirm_confirmed_subscription(self):
        self.subscription.confirmed = True
        self.subscription.confirmed_at = timezone.now()
        self.subscription.save()

        response = self.client.put(
            f"/subscription/confirmation/{urllib.parse.quote(self.signed_token)}",
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response_json["confirmation_token"][0], "token is invalid")

    def test_user_cannot_use_unknown_subscription_confirmation_token(self):
        response = self.client.put(
            "/subscription/confirmation/goofytoken",
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response_json["detail"], "No Subscription matches the given query."
        )


class AuthenticatedSubscriptionTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(email="user@example.org")
        self.subscriber = UserFactory(email="subscriber@gmail.com")
        self.client.cookies[settings.SIMPLE_JWT["AUTH_COOKIE"]] = RefreshToken.for_user(
            self.user
        ).access_token

    def test_authenticated_user_can_list_subscriptions(self):
        SubscriptionFactory(user=self.user, email=self.subscriber.email, active=True)
        response = self.client.get("/dashboard/subscriptions", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["email"], self.subscriber.email)

    def test_authenticated_user_cannot_list_inactive_subscriptions(self):
        SubscriptionFactory(user=self.user, email=self.subscriber.email, active=False)
        response = self.client.get("/dashboard/subscriptions", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, [])
        self.assertEqual(
            Subscription.objects.all().first().email, self.subscriber.email
        )
