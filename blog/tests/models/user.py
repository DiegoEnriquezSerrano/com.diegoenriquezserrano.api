from django.test import TestCase

from blog.models.profile import Profile
from blog.models.user import User

from blog.tests.factories.post_factory import PostFactory


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", username="testuser", password="testpassword"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("testpassword"))

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")

    def test_user_profile_creation(self):
        profile = Profile.objects.get(user=self.user)

        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, self.user)

    def test_user_posts(self):
        post = PostFactory(
            title="Test Post", body="This is a test post.", user=self.user
        )
        user_posts = self.user.posts()

        self.assertIn(post, user_posts)
        self.assertEqual(len(user_posts), 1)

    def test_user_email_unique(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="testuser@example.com",
                username="anotheruser",
                password="anotherpassword",
            )

    def test_user_username_unique(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                email="anotheruser@example.com",
                username="testuser",
                password="anotherpassword",
            )
