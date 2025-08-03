from rest_framework import serializers

from blog.models import Comment, Post

from .profile_serializer import ProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    profile = ProfileSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = [
            "body",
            "created_on",
            "id",
            "post_title",
            "post",
            "profile",
        ]
        depth = 1

    def get_post_title(self, comment):
        return comment.post.title

    def get_profile(self, comment):
        return comment.user.profile


class NotificationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "body",
            "created_on",
            "id",
        ]
