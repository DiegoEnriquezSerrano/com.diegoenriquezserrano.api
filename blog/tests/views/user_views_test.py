import json

from rest_framework import status
from rest_framework.test import APITestCase

from blog.tests.factories import UserFactory


class UserTests(APITestCase):
    def test_user_can_retrieve_profile_by_username(self):
        user = UserFactory()
        response = self.client.get(f"/user/profile/{user.username}", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["username"], user.username)
