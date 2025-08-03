from rest_framework import serializers


class AuthorSerializer(serializers.Serializer):
    likes = serializers.IntegerField(default=0)
    posts = serializers.IntegerField(default=0)
    bookmarks = serializers.IntegerField(default=0)
