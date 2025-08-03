import json

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from blog.models import Bookmark
from blog.tests.factories import BookmarkFactory, PostFactory, UserFactory


class AuthenticatedBookmarkTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.cookies["access_token"] = access_token
        self.post = PostFactory()

    def test_authenticated_user_can_list_bookmarks(self):
        bookmark = BookmarkFactory(user=self.user)
        response = self.client.get("/dashboard/bookmarks", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], bookmark.id)

    def test_authenticated_user_can_create_bookmark(self):
        response = self.client.post(
            "/posts/bookmark", {"post_id": self.post.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = json.loads(response.content)
        self.assertEqual(Bookmark.objects.count(), 1)
        self.assertEqual(response_json["message"], "bookmarked")

    def test_authenticated_user_can_delete_bookmark(self):
        BookmarkFactory(post=self.post, user=self.user)
        self.assertEqual(Bookmark.objects.count(), 1)

        response = self.client.post(
            "/posts/bookmark", {"post_id": self.post.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = json.loads(response.content)
        self.assertEqual(Bookmark.objects.count(), 0)
        self.assertEqual(response_json["message"], "unbookmarked")
