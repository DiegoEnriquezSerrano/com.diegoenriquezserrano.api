from marko import Markdown, Parser
from marko.md_renderer import MarkdownRenderer

from rest_framework import serializers

from blog.models import Project, User

from .profile_serializer import ProfileSerializer


class ProjectSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, many=False, required=False)

    class Meta:
        depth = 1
        fields = [
            "body",
            "cover_image_url",
            "created_at",
            "description",
            "finished_at",
            "profile",
            "slug",
            "started_at",
            "status",
            "title",
            "tools",
            "url",
        ]
        model = Project

    def get_profile(self, project):
        return project.user.profile


class CreateProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Project
        fields = [
            "body",
            "cover_image_url",
            "description",
            "finished_at",
            "started_at",
            "status",
            "title",
            "tools",
            "url",
            "user",
        ]

    def validate(self, data):
        if data.get("body") is not None:
            md_to_md = Markdown(renderer=MarkdownRenderer)
            self.body = md_to_md(data.get("body"))

        super().validate(data)

        return data
