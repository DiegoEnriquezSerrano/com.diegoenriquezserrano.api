import json

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from blog.models import UserSubscription
from blog.tests.factories import UserFactory


class AuthenticatedUserSubscriptionTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(email="user@example.org")
        self.subscriber = UserFactory(email="subscriber@gmail.com")
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.cookies["access_token"] = access_token

    def test_authenticated_user_can_list_subscriptions(self):
        UserSubscription.objects.create(
            user=self.user, subscriber=self.subscriber, active=True
        )
        response = self.client.get("/dashboard/user_subscriptions", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json[0]["subscriber"]["username"], self.subscriber.username
        )

    def test_authenticated_user_cannot_list_inactive_user_subscriptions(self):
        UserSubscription.objects.create(
            user=self.user, subscriber=self.subscriber, active=False
        )
        response = self.client.get("/dashboard/user_subscriptions", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, [])
        self.assertEqual(
            UserSubscription.objects.all().first().subscriber.username,
            self.subscriber.username,
        )

    def test_authenticated_user_can_create_user_subscription(self):
        response = self.client.post(
            f"/dashboard/subscribe/{self.subscriber.username}",
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserSubscription.objects.count(), 1)
        self.assertEqual(
            UserSubscription.objects.get(id=response_json["id"]).user,
            self.subscriber,
        )

    def test_authenticated_user_can_unsubscribe(self):
        user_subscription = UserSubscription.objects.create(
            user=self.user, subscriber=self.subscriber, active=True
        )

        response = self.client.put(
            f"/dashboard/user_subscriptions/{user_subscription.id}",
            {"active": False},
            format="json",
        )
        user_subscription.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserSubscription.objects.count(), 1)
        self.assertEqual(user_subscription.user, self.user)
        self.assertEqual(user_subscription.active, False)
