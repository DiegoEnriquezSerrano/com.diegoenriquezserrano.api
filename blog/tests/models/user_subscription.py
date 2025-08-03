from django.core.exceptions import ValidationError
from django.test import TestCase

from blog.models import UserSubscription
from blog.tests.factories import UserFactory


class UserSubscriptionModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.subscriber = UserFactory()

    def test_running_clean_sets_user_subscription_activation_dates(self):
        user_subscription = UserSubscription(
            subscriber=self.subscriber, user=self.user, active=False
        )

        self.assertIsNone(user_subscription.activated_date)
        self.assertIsNone(user_subscription.deactivated_date)

        user_subscription.full_clean()

        self.assertIsNone(user_subscription.activated_date)
        self.assertIsNotNone(user_subscription.deactivated_date)

    def test_saving_record_sets_user_subscription_activation_dates(self):
        user_subscription = UserSubscription(
            subscriber=self.subscriber, user=self.user, active=False
        )

        self.assertIsNone(user_subscription.activated_date)
        self.assertIsNone(user_subscription.deactivated_date)

        user_subscription.save()
        user_subscription.refresh_from_db()

        self.assertIsNone(user_subscription.activated_date)
        self.assertIsNotNone(user_subscription.deactivated_date)

    def test_creating_record_sets_activation_dates(self):
        user_subscription = UserSubscription.objects.create(
            subscriber=self.subscriber, user=self.user, active=False
        )

        self.assertIsNone(user_subscription.activated_date)
        self.assertIsNotNone(user_subscription.deactivated_date)

    def test_user_cannot_self_subscribe(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Cannot self-subscribe",
        ):
            UserSubscription(subscriber=self.user, user=self.user).full_clean()
