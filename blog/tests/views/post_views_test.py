import json

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from blog.models import Post
from blog.tests.factories import CategoryFactory, PostFactory, UserFactory


class AuthenticatedPostTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.cookies["access_token"] = access_token

    def test_authenticated_user_can_list_posts(self):
        category = CategoryFactory(user=self.user)
        post = PostFactory.create(user=self.user, categories=[category])
        response = self.client.get("/dashboard/posts", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["title"], post.title)

    def test_authenticated_user_can_create_post(self):
        response = self.client.post(
            "/dashboard/posts",
            {
                "title": "updated title",
                "description": "description",
                "body": "body",
                "cover_image_url": "http://www.example.com/home.png",
                "excerpt": "excerpt",
            },
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json["title"], "updated title")
        self.assertEqual(
            response_json["cover_image_url"], "http://www.example.com/home.png"
        )

    def test_authenticated_user_cannot_create_post_with_duplicate_title(self):
        PostFactory(title="updated title", user=self.user)
        response = self.client.post(
            "/dashboard/posts",
            {
                "title": "updated title",
                "description": "description",
                "body": "body",
                "cover_image_url": "http://www.example.com/home.png",
                "excerpt": "excerpt",
            },
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_json["title"][0], "post with this title already exists."
        )

    def test_authenticated_user_can_update_post(self):
        category = CategoryFactory(user=self.user)
        post = PostFactory.create(user=self.user, categories=[category])
        response = self.client.put(
            f"/dashboard/posts/{post.slug}",
            {
                "title": "updated title",
                "description": post.description,
                "body": post.body,
                "cover_image_url": post.cover_image_url,
                "excerpt": post.excerpt,
            },
            format="json",
        )
        response_json = json.loads(response.content)
        post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["title"], post.title)

    def test_authenticated_user_can_partial_update_post(self):
        category = CategoryFactory(user=self.user)
        post = PostFactory.create(user=self.user, categories=[category])
        response = self.client.patch(
            f"/dashboard/posts/{post.slug}", {"title": "updated title"}, format="json"
        )
        response_json = json.loads(response.content)
        post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["title"], post.title)

    def test_authenticated_user_can_like_post(self):
        post = PostFactory.create(user=self.user)
        response = self.client.post("/posts/like", {"post_id": post.id}, format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json["message"], "liked")

    def test_authenticated_user_can_unlike_post(self):
        post = PostFactory.create(user=self.user)
        post.likes.add(self.user)
        response = self.client.post("/posts/like", {"post_id": post.id}, format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["message"], "unliked")

    def test_authenticated_user_can_list_posts_by_category(self):
        category = CategoryFactory(user=self.user)
        post = PostFactory.create(user=self.user, categories=[category])
        response = self.client.get(
            f"/dashboard/categories/{category.slug}/posts", format="json"
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["title"], post.title)

    def test_authenticated_user_can_list_drafts(self):
        category = CategoryFactory(user=self.user)
        post = PostFactory.create(user=self.user, categories=[category], draft=True)
        response = self.client.get(f"/dashboard/post_drafts", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["title"], post.title)


class PostTests(APITestCase):
    def test_user_can_list_posts(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        post = PostFactory.create(user=user, categories=[category])
        response = self.client.get("/posts", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Post.objects.get(slug=response.data[0]["slug"], user__id=user.id).title,
            post.title,
        )

    def test_user_can_list_posts_by_username(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        post = PostFactory.create(user=user, categories=[category])
        response = self.client.get(f"/posts/{user.username}", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["slug"], post.slug)

    def test_get_posts_by_user_path_empty_if_username_does_not_exist(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        PostFactory.create(user=user, categories=[category])
        response = self.client.get(f"/posts/{user.username}1234", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, [])

    def test_user_can_retrieve_post(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        post = PostFactory.create(user=user, categories=[category])
        response = self.client.get(f"/posts/{user.username}/{post.slug}", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["title"], post.title)

    def test_get_post_detail_path_not_found_if_username_does_not_exist(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        post = PostFactory.create(user=user, categories=[category])
        response = self.client.get(
            f"/posts/{user.username}1234/{post.slug}", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_detail_path_not_found_if_slug_does_not_exist(self):
        user = UserFactory()
        category = CategoryFactory(user=user)
        post = PostFactory.create(user=user, categories=[category])
        response = self.client.get(
            f"/posts/{user.username}/{post.slug}1234", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
