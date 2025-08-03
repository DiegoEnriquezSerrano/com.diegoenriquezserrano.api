from rest_framework import serializers

from blog.models import Notification

from .comment_serializer import NotificationCommentSerializer
from .post_serializer import NotificationPostSerializer
from .profile_serializer import ProfileSerializer


class NotificationSerializer(serializers.ModelSerializer):
    comment = NotificationCommentSerializer(read_only=True, many=False, required=False)
    post = NotificationPostSerializer(many=False)
    profile = ProfileSerializer(read_only=True, many=False, required=False)

    class Meta:
        model = Notification
        fields = ["id", "read", "type", "post", "comment", "profile"]
        depth = 1

    def get_profile(self):
        return self.user.profile
