from django.utils.text import slugify

from rest_framework import serializers

from blog.models import Post, Category, User

from .category_serializer import CategorySerializer
from .comment_serializer import CommentSerializer
from .profile_serializer import ProfileSerializer
from .user_serializer import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False, read_only=True)
    profile = ProfileSerializer(required=False, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "body",
            "categories",
            "comments",
            "cover_image_url",
            "created_on",
            "description",
            "excerpt",
            "featured",
            "last_modified",
            "profile",
            "slug",
            "title",
            "user",
        ]

    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    def get_profile(self, post):
        return post.user.profile


class CreatePostSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, many=True
    )
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = [
            "body",
            "categories",
            "cover_image_url",
            "description",
            "draft",
            "excerpt",
            "featured",
            "title",
            "user",
        ]

    def validate(self, data):
        self.slug = slugify(data["title"])

        super().validate(data)

        return data


class NotificationPostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False, read_only=True)

    class Meta:
        model = Post
        depth = 0
        fields = ["id", "title", "cover_image_url", "excerpt", "slug", "profile"]

    def get_profile(self, post):
        return post.user.profile
