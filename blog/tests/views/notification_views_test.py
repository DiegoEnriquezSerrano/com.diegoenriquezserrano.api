import json

from django.conf import settings

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from blog.tests.factories import NotificationFactory, PostFactory, UserFactory


class AuthenticatedNotificationTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.cookies[settings.SIMPLE_JWT["AUTH_COOKIE"]] = RefreshToken.for_user(
            self.user
        ).access_token
        self.post = PostFactory(user=self.user)

    def test_authenticated_user_can_list_notifications(self):
        notification = NotificationFactory(post=self.post)
        response = self.client.get("/dashboard/notifications", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["type"], notification.type)

    def test_authenticated_user_can_update_notification(self):
        notification = NotificationFactory(post=self.post)
        response = self.client.put(
            f"/dashboard/notifications/{notification.id}", format="json"
        )
        response_json = json.loads(response.content)
        notification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["message"], "notification read")
        self.assertEqual(notification.read, True)

    def test_authenticated_user_can_partial_update_notification(self):
        notification = NotificationFactory(post=self.post)
        response = self.client.patch(
            f"/dashboard/notifications/{notification.id}", format="json"
        )
        response_json = json.loads(response.content)
        notification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["message"], "notification read")
        self.assertEqual(notification.read, True)
