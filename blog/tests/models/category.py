from django.test import TestCase

from blog.models import Category, User, Post
from blog.tests.factories import PostFactory, UserFactory


class CategoryModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")

    def test_category_creation(self):
        category = Category.objects.create(name="Test Category", user=self.user)

        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.slug, "test-category")

    def test_post_count(self):
        category = Category.objects.create(name="Test Category", user=self.user)
        PostFactory(categories=[category], user=self.user, draft=True)
        PostFactory(categories=[category], user=self.user, draft=False)
        PostFactory(categories=[category], user=self.user, draft=False)

        self.assertEqual(category.post_count(), 2)

    def test_find_by_slug_and_username(self):
        category = Category.objects.create(name="Test Category", user=self.user)
        found_category = Category.find_by_slug_and_username(
            category.slug, self.user.username
        )
        self.assertEqual(found_category, category)

    def test_find_list_by_username(self):
        Category.objects.create(name="Category 1", user=self.user)
        Category.objects.create(name="Category 2", user=self.user)
        other_user = UserFactory(username="otheruser")
        Category.objects.create(name="Category 3", user=other_user)
        user_categories = Category.find_list_by_username(self.user.username)

        self.assertEqual(user_categories.count(), 2)
        self.assertTrue(all(cat.user == self.user for cat in user_categories))

    def test_unique_together_constraint(self):
        Category.objects.create(name="Unique Category", user=self.user)

        with self.assertRaises(Exception):
            Category.objects.create(name="Unique Category", user=self.user)
