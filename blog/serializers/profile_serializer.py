from rest_framework import serializers

from blog.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        fields = [
            "banner",
            "bio",
            "bluesky",
            "description",
            "github",
            "image",
            "linkedin",
            "mastodon",
            "twitch",
            "username",
            "youtube",
        ]
        model = Profile

    def get_username(self, profile):
        return profile.user.username
