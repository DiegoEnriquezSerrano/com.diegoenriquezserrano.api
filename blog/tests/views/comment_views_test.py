import json

from django.conf import settings

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from blog.models import Comment, Notification
from blog.tests.factories import CommentFactory, PostFactory, UserFactory


class AuthenticatedCommentTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.cookies[settings.SIMPLE_JWT["AUTH_COOKIE"]] = RefreshToken.for_user(
            self.user
        ).access_token
        self.post = PostFactory()

    def test_authenticated_user_can_create_comment(self):
        response = self.client.post(
            "/posts/comment", {"post_id": self.post.id, "body": "test"}, format="json"
        )
        response_json = json.loads(response.content)
        notification = Notification.objects.all().last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get(id=response_json["id"]).body, "test")
        self.assertEqual(
            Comment.objects.get(id=response_json["id"]).post_id, self.post.id
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.post, self.post)
        self.assertEqual(notification.type, "comment")
        self.assertNotEqual(notification.user, self.post.user)

    def test_authenticated_user_can_list_comments(self):
        mypost = PostFactory(user=self.user)
        comment = CommentFactory(user=self.user, post=mypost)
        response = self.client.get("/dashboard/comments", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["body"], comment.body)

    def test_authenticated_user_can_view_comment(self):
        mypost = PostFactory(user=self.user)
        comment = CommentFactory(user=self.user, post=mypost)
        response = self.client.get(f"/dashboard/comments/{comment.id}", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["body"], comment.body)

    def test_authenticated_user_can_delete_comment(self):
        mypost = PostFactory(user=self.user)
        comment = CommentFactory(user=self.user, post=mypost)
        response = self.client.delete(
            f"/dashboard/comments/{comment.id}", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
