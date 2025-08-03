import json

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from blog.tests.factories import UserFactory


class AuthenticatedProfileTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.cookies["access_token"] = access_token

    def test_authenticated_user_can_retrieve_profile(self):
        profile = self.user.profile
        response = self.client.get("/dashboard/profile", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["description"], profile.description)

    def test_authenticated_user_can_update_profile(self):
        profile = self.user.profile
        response = self.client.put(
            "/dashboard/profile",
            {
                "description": "updated title",
            },
            format="json",
        )
        response_json = json.loads(response.content)
        profile.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["description"], "updated title")
