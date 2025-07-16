from rest_framework import serializers

from blog.models import Category

from .user_serializer import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        depth = 1
        model = Category
        fields = ["id", "name", "slug", "post_count", "user"]

    def get_post_count(self, category):
        return category.posts.count()
