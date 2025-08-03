from django.test import TestCase

from blog.models import UserSubscription
from blog.serializers import (
    CreateUserSubscriptionSerializer,
)
from blog.tests.factories import UserFactory


class UserSubscriptionSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser", email="user@example.com")
        self.subscriber = UserFactory(
            username="testsubscriber", email="subscriber@example.com"
        )

    def test_valid_subscription(self):
        serializer = CreateUserSubscriptionSerializer(
            data={
                "subscriber": self.subscriber.id,
                "user": self.user.id,
                "active": True,
            }
        )

        serializer.is_valid()

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["subscriber"], self.subscriber)
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_missing_subscriber(self):
        data = {"user": self.user.id, "active": True}

        serializer = CreateUserSubscriptionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("subscriber", serializer.errors)

    def test_missing_user(self):
        data = {
            "subscriber": self.subscriber.id,
            "active": True,
        }

        serializer = CreateUserSubscriptionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)

    def test_missing_active(self):
        data = {
            "subscriber": self.subscriber.id,
            "user": self.user.id,
            "active": None,
        }

        serializer = CreateUserSubscriptionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("active", serializer.errors)

    def test_unique_subscriber_per_user(self):
        UserSubscription.objects.create(
            subscriber=self.subscriber, active=True, user=self.user
        )

        data = {
            "subscriber": self.subscriber.id,
            "user": self.user.id,
            "active": True,
        }
        serializer = CreateUserSubscriptionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "The fields user, subscriber must make a unique set.",
        )

    def test_cannot_self_subscribe(self):
        serializer = CreateUserSubscriptionSerializer(
            data={
                "subscriber": self.user.id,
                "user": self.user.id,
                "active": True,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0], "Cannot self-subscribe"
        )
