from django.test import TestCase
from django.utils import timezone

from blog.models import UserSubscription
from blog.serializers import ProfileSerializer
from blog.tests.factories import UserFactory


class ProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.profile = self.user.profile
        self.profile.bio = "This is a bio."
        self.profile.description = "This is a description."
        self.profile.image = "http://example.com/test.png"
        self.profile.banner = "https://example.com/banner.jpg"
        self.profile.bluesky = "testuser.bsky.app"
        self.profile.github = "https://github.com/testuser"
        self.profile.linkedin = "https://linkedin.com/in/testuser"
        self.profile.mastodon = "https://mastodon.example.com/@testuser"
        self.profile.twitch = "https://twitch.tv/testuser"
        self.profile.youtube = "https://youtube.com/testuser"
        self.profile.save()

    def test_profile_serializer(self):
        serializer = ProfileSerializer(instance=self.profile)
        data = serializer.data

        self.assertEqual(data["banner"], self.profile.banner)
        self.assertEqual(data["bio"], self.profile.bio)
        self.assertEqual(data["bluesky"], self.profile.bluesky)
        self.assertEqual(data["description"], self.profile.description)
        self.assertEqual(data["github"], self.profile.github)
        self.assertEqual(data["image"], self.profile.image)
        self.assertEqual(data["linkedin"], self.profile.linkedin)
        self.assertEqual(data["mastodon"], self.profile.mastodon)
        self.assertEqual(data["twitch"], self.profile.twitch)
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["youtube"], self.profile.youtube)

    def test_profile_subscription_counts(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        user4 = UserFactory()

        self.user.subscribers.set(
            [user1, user4],
            through_defaults={"activated_date": timezone.now(), "active": True},
        )
        self.user.subscribed.set(
            [user2, user3],
            through_defaults={"activated_date": timezone.now(), "active": True},
        )
        self.user.save()

        deactivated = UserSubscription.objects.get(
            user_id=self.user.id, subscriber_id=user4.id
        )
        deactivated.active = False
        deactivated.save()

        serializer = ProfileSerializer(instance=self.profile)
        data = serializer.data

        self.assertEqual(data["subscribers_count"], 1)
        self.assertEqual(data["subscribed_count"], 2)
