from django.test import TestCase

from blog.models.bookmark import Bookmark
from blog.tests.factories import UserFactory, PostFactory, BookmarkFactory


class BookmarkModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory()

    def test_bookmark_creation(self):
        bookmark = Bookmark.objects.create(user=self.user, post=self.post)

        self.assertEqual(bookmark.user, self.user)
        self.assertEqual(bookmark.post, self.post)

    def test_bookmark_str(self):
        bookmark = BookmarkFactory(user=self.user, post=self.post)

        self.assertEqual(str(bookmark), self.post.title)

    def test_create_or_delete_create(self):
        result = Bookmark.create_or_delete(self.user, self.post.id)

        self.assertEqual(result, "created")
        self.assertTrue(
            Bookmark.objects.filter(user=self.user, post=self.post).exists()
        )

    def test_create_or_delete_delete(self):
        Bookmark.objects.create(user=self.user, post=self.post)
        result = Bookmark.create_or_delete(self.user, self.post.id)

        self.assertEqual(result, "deleted")
        self.assertFalse(
            Bookmark.objects.filter(user=self.user, post=self.post).exists()
        )

    def test_create_or_delete_nonexistent_post(self):
        with self.assertRaises(Exception):
            Bookmark.create_or_delete(self.user, 999)
