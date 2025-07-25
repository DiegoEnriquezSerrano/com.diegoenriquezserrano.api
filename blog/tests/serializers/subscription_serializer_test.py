from django.test import TestCase

from blog.serializers import SubscriptionSerializer
from blog.tests.factories import UserFactory, SubscriptionFactory


class SubscriptionSerializerTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser", email="user@example.com")

    def test_valid_subscription(self):
        serializer = SubscriptionSerializer(
            data={
                "email": "user@testsubscriber.com",
                "name": "Test Subscriber",
                "user": self.user.id,
                "active": True,
            }
        )

        serializer.is_valid()

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["email"], "user@testsubscriber.com")
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_missing_email(self):
        data = {"name": "Test Subscriber", "user": self.user.id, "active": True}

        serializer = SubscriptionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_invalid_email(self):
        data = {
            "name": "Test Subscriber",
            "user": self.user.id,
            "active": True,
            "email": "example.com",
        }

        serializer = SubscriptionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_missing_user(self):
        data = {
            "email": "subscriber@example.com",
            "name": "Test Subscriber",
            "active": True,
        }

        serializer = SubscriptionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("user", serializer.errors)

    def test_unique_email_per_user(self):
        SubscriptionFactory(
            email="subscriber@example.com", name="First Subscriber", user=self.user
        )

        data = {
            "email": "subscriber@example.com",
            "name": "Second Subscriber",
            "user": self.user.id,
            "active": True,
        }
        serializer = SubscriptionSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "The fields user, email must make a unique set.",
        )

    def test_cannot_self_subscribe(self):
        serializer = SubscriptionSerializer(
            data={
                "email": "user@example.com",
                "name": "Test Subscriber",
                "user": self.user.id,
                "active": True,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0], "Cannot self-subscribe"
        )
