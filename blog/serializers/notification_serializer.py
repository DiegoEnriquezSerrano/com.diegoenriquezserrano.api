from rest_framework import serializers

from blog.models import Notification

from .user_serializer import UserSerializer
from .post_serializer import PostSerializer


class NotificationSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=False)
    user = UserSerializer(read_only=True)

    class Meta:
        depth = 1
        fields = fields = ["id", "read", "type", "post", "user"]
        model = Notification
