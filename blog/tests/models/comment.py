from django.test import TestCase

from blog.models import Comment, Post, User
from blog.tests.factories import UserFactory, PostFactory


class CommentModelTests(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(user=self.user)

    def test_comment_creation(self):
        comment = Comment.objects.create(
            body="This is a test comment.", post=self.post, user=self.user
        )

        self.assertEqual(comment.body, "This is a test comment.")
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.user, self.user)

    def test_comment_str(self):
        comment = Comment.objects.create(
            body="Another test comment.", post=self.post, user=self.user
        )

        self.assertEqual(str(comment), f"{self.post.title}__Another test comment.")

    def test_comment_ordering(self):
        comment1 = Comment.objects.create(
            body="First comment.", post=self.post, user=self.user
        )
        comment2 = Comment.objects.create(
            body="Second comment.", post=self.post, user=self.user
        )
        comments = Comment.objects.all()

        self.assertEqual(list(comments), [comment2, comment1])

    def test_comment_auto_dates(self):
        comment = Comment.objects.create(
            body="Test comment with auto dates.", post=self.post, user=self.user
        )

        self.assertIsNotNone(comment.created_on)
        self.assertIsNotNone(comment.date)
        self.assertIsNotNone(comment.last_modified)

    def test_comment_max_length(self):
        with self.assertRaises(Exception):
            comment = Comment(body="x" * 501, post=self.post, user=self.user)
            comment.full_clean()
