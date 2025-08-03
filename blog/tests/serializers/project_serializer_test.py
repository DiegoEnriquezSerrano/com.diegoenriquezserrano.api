from django.test import TestCase
from django.utils import timezone

from blog.serializers import ProjectSerializer, CreateProjectSerializer
from blog.tests.factories import UserFactory, ProjectFactory


class ProjectSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.project = ProjectFactory(user=self.user)

    def test_project_serializer(self):
        serializer = ProjectSerializer(instance=self.project)
        data = serializer.data

        self.assertEqual(data["body"], self.project.body)
        self.assertEqual(data["cover_image_url"], self.project.cover_image_url)
        self.assertEqual(
            data["created_at"],
            self.project.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        self.assertEqual(data["description"], self.project.description)
        self.assertEqual(data["finished_at"], self.project.finished_at)
        self.assertEqual(data["slug"], self.project.slug)
        self.assertEqual(
            data["started_at"],
            self.project.started_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )
        self.assertEqual(data["status"], self.project.status)
        self.assertEqual(data["title"], self.project.title)
        self.assertEqual(data["tools"], self.project.tools)
        self.assertEqual(data["url"], self.project.url)
        self.assertEqual(data["profile"]["username"], self.user.username)


class CreateProjectSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.data = {
            "body": "this is a test body",
            "cover_image_url": "https://example.org/logo.png",
            "description": "this is a test description",
            "finished_at": None,
            "started_at": timezone.now(),
            "status": "ongoing",
            "title": "this is a test title",
            "tools": ["django", "postgresql"],
            "url": "https://example.org/projects/first-project",
            "user": self.user.id,
        }

    def test_create_project_serializer(self):
        serializer = CreateProjectSerializer(data=self.data)
        serializer.is_valid()
        result = serializer.validated_data

        self.assertEqual(result["body"], self.data["body"])
        self.assertEqual(result["cover_image_url"], self.data["cover_image_url"])
        self.assertEqual(result["description"], self.data["description"])
        self.assertEqual(result["finished_at"], self.data["finished_at"])
        self.assertEqual(result["started_at"], self.data["started_at"])
        self.assertEqual(result["status"], self.data["status"])
        self.assertEqual(result["title"], self.data["title"])
        self.assertEqual(result["tools"], self.data["tools"])
        self.assertEqual(result["url"], self.data["url"])
        self.assertEqual(result["user"], self.user)
