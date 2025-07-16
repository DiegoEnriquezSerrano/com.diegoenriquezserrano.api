from rest_framework import serializers

from blog.models.bookmark import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        fields = ["id", "post", "user"]
        model = Bookmark
