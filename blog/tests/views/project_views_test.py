import json

from django.utils import timezone

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from blog.models import Project
from blog.tests.factories import ProjectFactory, UserFactory


class ProjectTests(APITestCase):
    def test_user_can_list_projects(self):
        user = UserFactory()
        project = ProjectFactory(user=user)
        response = self.client.get("/projects", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Project.objects.get(slug=response.data[0]["slug"], user__id=user.id).title,
            project.title,
        )

    def test_user_can_list_projects_by_username(self):
        user = UserFactory()
        project = ProjectFactory(user=user)
        response = self.client.get(f"/projects/{user.username}", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["slug"], project.slug)

    def test_user_can_retrieve_project(self):
        user = UserFactory()
        project = ProjectFactory(user=user)
        response = self.client.get(
            f"/projects/{user.username}/{project.slug}", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], project.title)

    def test_get_projects_by_user_path_empty_list_if_username_does_not_exist(self):
        user = UserFactory()
        ProjectFactory(user=user)
        response = self.client.get(f"/projects/{user.username}1234", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, [])

    def test_get_project_detail_path_not_found_if_username_does_not_exist(self):
        user = UserFactory()
        project = ProjectFactory(user=user)
        response = self.client.get(
            f"/projects/{user.username}1234/{project.slug}", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_project_detail_path_not_found_if_slug_does_not_exist(self):
        user = UserFactory()
        project = ProjectFactory(user=user)
        response = self.client.get(
            f"/projects/{user.username}/{project.slug}1234", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthenticatedProjectTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        self.client.cookies["access_token"] = access_token

    def test_authenticated_user_can_list_projects(self):
        project = ProjectFactory.create(user=self.user)
        response = self.client.get("/dashboard/projects", format="json")
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]["title"], project.title)

    def test_authenticated_user_can_create_project(self):
        response = self.client.post(
            "/dashboard/projects",
            {
                "body": "this is a test body",
                "cover_image_url": "https://example.org/logo.png",
                "description": "this is a test description",
                "finished_at": None,
                "started_at": timezone.now(),
                "status": "ongoing",
                "title": "this is a test title",
                "tools": ["django", "postgresql"],
                "url": "https://example.org/projects/first-project",
            },
            format="json",
        )
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_json["title"], "this is a test title")
        self.assertEqual(response_json["profile"]["username"], self.user.username)

    def test_authenticated_user_can_update_project(self):
        project = ProjectFactory.create(user=self.user)
        response = self.client.put(
            f"/dashboard/projects/{project.slug}",
            {
                "body": project.body,
                "cover_image_url": project.cover_image_url,
                "description": project.description,
                "started_at": project.started_at,
                "status": project.status,
                "title": "updated title",
            },
            format="json",
        )
        response_json = json.loads(response.content)
        project.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["title"], "updated title")

    def test_authenticated_user_can_partial_update_project(self):
        project = ProjectFactory.create(user=self.user)
        response = self.client.patch(
            f"/dashboard/projects/{project.slug}",
            {"title": "updated title"},
            format="json",
        )
        response_json = json.loads(response.content)
        project.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json["title"], project.title)

    def test_authenticated_user_can_delete_project(self):
        project = ProjectFactory(user=self.user)
        response = self.client.delete(
            f"/dashboard/projects/{project.slug}", format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
