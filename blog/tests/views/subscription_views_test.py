import json

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from blog.models import Subscription
from blog.tests.factories import UserFactory


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(email="user@example.org")

    def test_unauthenticated_user_can_create_subscription(self):
        response = self.client.post(
            f"/subscribe/{self.user.username}",
            {"email": "newsubscriber@company.com"},
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(
            Subscription.objects.get(id=response_json["id"]).email,
            "newsubscriber@company.com",
        )

    def test_cannot_create_duplicate_subscription(self):
        Subscription.objects.create(user=self.user, email="newsubscriber@company.com")

        response = self.client.post(
            f"/subscribe/{self.user.username}",
            {"email": "newsubscriber@company.com"},
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["non_field_errors"][0],
            "The fields user, email must make a unique set.",
        )

    def test_cannot_unauthenticated_user_cannot_self_subscribe(self):
        response = self.client.post(
            f"/subscribe/{self.user.username}",
            {"email": self.user.email},
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["non_field_errors"][0],
            "Cannot self-subscribe",
        )


class AuthenticatedSubscriptionTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(email="user@example.org")
        self.subscriber = UserFactory(email="subscriber@gmail.com")
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.cookies["access_token"] = access_token

    def test_authenticated_user_can_list_subscriptions(self):
        Subscription.objects.create(
            user=self.user, email=self.subscriber.email, active=True
        )
        response = self.client.get("/dashboard/subscriptions", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["email"], self.subscriber.email)

    def test_authenticated_user_cannot_list_inactive_subscriptions(self):
        Subscription.objects.create(
            user=self.user, email=self.subscriber.email, active=False
        )
        response = self.client.get("/dashboard/subscriptions", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, [])
        self.assertEqual(
            Subscription.objects.all().first().email, self.subscriber.email
        )
