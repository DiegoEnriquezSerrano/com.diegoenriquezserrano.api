from django.test import TestCase
from blog.serializers import CategorySerializer
from blog.tests.factories import UserFactory, CategoryFactory


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser", email="test@example.com")
        self.category = CategoryFactory(
            name="Test Category", slug="test-category", user=self.user
        )
        self.category.posts.create(
            title="Post 1", body="Content of post 1", user=self.user
        )
        self.category.posts.create(
            title="Post 2", body="Content of post 2", user=self.user
        )

    def test_category_serializer(self):
        serializer = CategorySerializer(instance=self.category)
        data = serializer.data

        self.assertEqual(data["id"], self.category.id)
        self.assertEqual(data["name"], self.category.name)
        self.assertEqual(data["slug"], self.category.slug)
        self.assertEqual(data["post_count"], 2)
        self.assertEqual(data["user"]["username"], self.user.username)

    def test_post_count_method(self):
        empty_category = CategoryFactory(
            name="Empty Category", slug="empty-category", user=self.user
        )
        serializer = CategorySerializer(instance=empty_category)
        data = serializer.data

        self.assertEqual(data["post_count"], 0)
