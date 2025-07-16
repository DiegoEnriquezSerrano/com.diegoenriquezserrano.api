from django.test import TestCase

from blog.serializers import ProfileSerializer
from blog.tests.factories import UserFactory


class ProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = self.user.profile
        self.profile.author = True
        self.profile.bio = "This is a bio."
        self.profile.bluesky = "https://bluesky.example.com/testuser"
        self.profile.github = "https://github.com/testuser"
        self.profile.linkedin = "https://linkedin.com/in/testuser"
        self.profile.mastodon = "https://mastodon.example.com/@testuser"
        self.profile.twitch = "https://twitch.tv/testuser"
        self.profile.youtube = "https://youtube.com/testuser"
        self.profile.save()

    def test_profile_serializer(self):
        serializer = ProfileSerializer(instance=self.profile)
        data = serializer.data

        self.assertEqual(data["author"], True)
        self.assertEqual(data["bio"], self.profile.bio)
        self.assertEqual(data["bluesky"], self.profile.bluesky)
        self.assertEqual(data["github"], self.profile.github)
        self.assertEqual(data["linkedin"], self.profile.linkedin)
        self.assertEqual(data["mastodon"], self.profile.mastodon)
        self.assertEqual(data["twitch"], self.profile.twitch)
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["youtube"], self.profile.youtube)
