import json

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from blog.models import Category
from blog.tests.factories import CategoryFactory, PostFactory, UserFactory


class CategoryTests(APITestCase):
    def test_user_can_list_categories(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        response = self.client.get("/categories", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Category.objects.get(slug=response_json[0]["slug"], user__id=user.id).name,
            category.name,
        )

    def test_user_can_list_categories_by_username(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        response = self.client.get(f"/categories/{user.username}", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["slug"], category.slug)

    def test_user_can_retrieve_category(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        response = self.client.get(
            f"/categories/{user.username}/{category.slug}", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], category.name)

    def test_user_can_list_category_posts(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        post = PostFactory.create(user=user, categories=[category])
        response = self.client.get(
            f"/categories/{user.username}/{category.slug}/posts", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], post.title)

    def test_get_categories_by_user_path_empty_list_if_username_does_not_exist(self):
        user = UserFactory()
        CategoryFactory(user=user)
        response = self.client.get(f"/categories/{user.username}1234", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, [])

    def test_get_category_detail_path_not_found_if_username_does_not_exist(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        response = self.client.get(
            f"/posts/{user.username}1234/{category.slug}", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_category_detail_path_not_found_if_slug_does_not_exist(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        response = self.client.get(
            f"/posts/{user.username}/{category.slug}1234", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_category_posts_path_not_found_if_username_does_not_exist(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        post = PostFactory.create(user=user, categories=[category])
        response = self.client.get(
            f"/posts/{user.username}1234/{post.slug}/posts", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_category_posts_path_not_found_if_slug_does_not_exist(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        post = PostFactory.create(user=user, categories=[category])
        response = self.client.get(
            f"/posts/{user.username}/{post.slug}1234/posts", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthenticatedCategoryTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.cookies["access_token"] = access_token

    def test_authenticated_user_can_create_category(self):
        response = self.client.post(
            "/dashboard/categories", {"name": "Battletoads"}, format="json"
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(
            Category.objects.get(id=response_json["id"]).slug, "battletoads"
        )

    def test_authenticated_user_cannot_create_duplicate_category(self):
        CategoryFactory(name="Battletoads", user=self.user)
        response = self.client.post(
            "/dashboard/categories", {"name": "Battletoads"}, format="json"
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["non_field_errors"][0],
            "The fields name, user must make a unique set.",
        )

    def test_authenticated_user_can_list_categories(self):
        category = CategoryFactory(user=self.user)
        response = self.client.get("/dashboard/categories", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["name"], category.name)

    def test_authenticated_user_can_retrieve_category(self):
        category = CategoryFactory(user=self.user)
        response = self.client.get(
            f"/dashboard/categories/{category.slug}", format="json"
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["name"], category.name)

    def test_authenticated_user_can_update_category(self):
        category = CategoryFactory(user=self.user)
        response = self.client.put(
            f"/dashboard/categories/{category.slug}",
            {
                "name": "updated title",
            },
            format="json",
        )
        response_json = json.loads(response.content)
        category.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["name"], "updated title")

    def test_authenticated_user_can_delete_category(self):
        category = CategoryFactory(user=self.user)
        response = self.client.delete(
            f"/dashboard/categories/{category.slug}", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
