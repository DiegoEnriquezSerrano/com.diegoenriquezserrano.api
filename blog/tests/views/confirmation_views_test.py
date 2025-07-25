import json

from django.core.signing import TimestampSigner
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from blog.tests.factories import UserFactory


class ConfirmationViewTests(APITestCase):
    def setUp(self):
        signer = TimestampSigner()
        user = UserFactory()
        user.confirmed = False
        user.confirmed_at = None
        user.save()

        self.user = user
        self.signed_token = signer.sign_object(
            {"confirmation_token": self.user.confirmation_token}
        )

    def test_user_can_confirm_with_valid_token(self):
        response = self.client.put(
            f"/user/confirmation/{self.signed_token}",
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.confirmed, True)
        self.assertEqual(response_json["message"], "user confirmation OK")

    def test_user_cannot_confirm_confirmed_user(self):
        self.user.confirmed = True
        self.user.confirmed_at = timezone.now()
        self.user.save()

        response = self.client.put(
            f"/user/confirmation/{self.signed_token}",
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response_json["message"], "confirmation token invalid")

    def test_user_cannot_use_unknown_token(self):
        response = self.client.put(
            "/user/confirmation/goofytoken",
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_json["detail"], "No User matches the given query.")
