from rest_framework import serializers

from blog.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    subscribed_count = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        fields = [
            "banner",
            "bio",
            "bluesky",
            "description",
            "display_name",
            "github",
            "image",
            "linkedin",
            "mastodon",
            "twitch",
            "username",
            "youtube",
            "subscribed_count",
            "subscribers_count",
        ]
        model = Profile

    def get_username(self, profile):
        return profile.user.username

    def get_subscribed_count(self, profile):
        return profile.user.total_active_subscribed()

    def get_subscribers_count(self, profile):
        return profile.user.total_active_subscribers()
