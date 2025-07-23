from django.core.exceptions import ValidationError
from django.test import TestCase

from blog.models import Subscription
from blog.tests.factories import UserFactory


class SubscriptionModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_running_clean_sets_activation_dates(self):
        subscription = Subscription(
            email="newuser@example.com", user=self.user, active=False
        )

        self.assertIsNone(subscription.activated_date)
        self.assertIsNone(subscription.deactivated_date)

        subscription.full_clean()

        self.assertIsNone(subscription.activated_date)
        self.assertIsNotNone(subscription.deactivated_date)

    def test_saving_record_sets_activation_dates(self):
        subscription = Subscription(
            email="newuser@example.com", user=self.user, active=False
        )

        self.assertIsNone(subscription.activated_date)
        self.assertIsNone(subscription.deactivated_date)

        subscription.save()
        subscription.refresh_from_db()

        self.assertIsNone(subscription.activated_date)
        self.assertIsNotNone(subscription.deactivated_date)

    def test_creating_record_sets_activation_dates(self):
        subscription = Subscription.objects.create(
            email="newuser@example.com", user=self.user, active=False
        )

        self.assertIsNone(subscription.activated_date)
        self.assertIsNotNone(subscription.deactivated_date)

    def test_unique_email_per_user(self):
        Subscription.objects.create(email="subscriber@example.com", user=self.user)

        with self.assertRaisesMessage(
            ValidationError, "Subscription with this User and Email already exists."
        ):
            Subscription(email="subscriber@example.com", user=self.user).full_clean()

    def test_user_cannot_self_subscribe(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Cannot self-subscribe",
        ):
            Subscription.objects.create(
                email=self.user.email, user=self.user
            ).full_clean()
