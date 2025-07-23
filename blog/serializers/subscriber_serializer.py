from rest_framework import serializers

from blog.models import UserSubscription


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ("id", "user_id", "activated_date", "active")
