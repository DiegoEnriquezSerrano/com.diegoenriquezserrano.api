from django.test import TestCase
from django.core.exceptions import ValidationError

from blog.models.post import Post

from blog.tests.factories.category_factory import CategoryFactory
from blog.tests.factories.post_factory import PostFactory
from blog.tests.factories.user_factory import UserFactory


class PostModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.category = CategoryFactory(name="Test Category", user=self.user)

    def test_post_creation(self):
        post = Post.objects.create(
            title="Test Post",
            body="This is a test post body.",
            description="This is a test description.",
            excerpt="This is a test excerpt.",
            cover_image_url="http://example.com/image.jpg",
            user=self.user,
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.body, "This is a test post body.")
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.slug, "test-post")

    def test_post_str(self):
        post = PostFactory(
            title="Another Test Post",
            user=self.user,
        )
        self.assertEqual(str(post), "Another Test Post")

    def test_toggle_like(self):
        post = PostFactory(user=self.user)
        result = post.toggle_like(self.user)

        self.assertEqual(result, "liked")
        self.assertIn(self.user, post.likes.all())

        result = post.toggle_like(self.user)

        self.assertEqual(result, "unliked")
        self.assertNotIn(self.user, post.likes.all())

    def test_find_by_slug_and_username(self):
        post = PostFactory(user=self.user)
        found_post = Post.find_by_slug_and_username(post.slug, self.user.username)

        self.assertEqual(found_post, post)

    def test_find_list_by_username(self):
        PostFactory(user=self.user)
        PostFactory(user=self.user)
        user_posts = Post.find_list_by_username(self.user.username)

        self.assertEqual(user_posts.count(), 2)

    def test_description_max_length(self):
        with self.assertRaises(ValidationError):
            post = Post(
                title="Test Post",
                body="This is a test post body.",
                description="x" * 201,
                excerpt="This is a test excerpt.",
                cover_image_url="http://example.com/image2.jpg",
                user=self.user,
            )
            post.full_clean()
