from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class UserSubscription(models.Model):
    user = models.ForeignKey(to="blog.User", on_delete=models.CASCADE, related_name="+")
    subscriber = models.ForeignKey(
        to="blog.User", on_delete=models.CASCADE, related_name="+"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, null=False)
    activated_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    deactivated_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    class Meta:
        ordering = ["-activated_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "subscriber"], name="unique_user_subscriptions"
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_subscribe",
                check=~models.Q(subscriber=models.F("user")),
            ),
            models.CheckConstraint(
                condition=models.Q(activated_date__isnull=False)
                | models.Q(deactivated_date__isnull=False),
                name="prevent_user_subscription_deactivated_and_activated_null",
            ),
            models.CheckConstraint(
                condition=models.Q(activated_date__isnull=True)
                | models.Q(deactivated_date__isnull=True),
                name="prevent_user_subscription_deactivated_and_activated_present",
            ),
            models.CheckConstraint(
                condition=models.Q(active=True, activated_date__isnull=False)
                | models.Q(active=False, deactivated_date__isnull=False),
                name="prevent_user_subscriptions_active_and_activated_date_null",
            ),
        ]
        indexes = [
            models.Index(
                fields=["user", "subscriber"],
                include=["active"],
                name="user_subscribers_idx",
            ),
            models.Index(
                fields=["subscriber", "user"],
                include=["active"],
                name="user_subscribed_idx",
            ),
        ]

    def __str__(self):
        return f"{self.subscriber.username} to {self.user.username}"

    def save(self, *args, **kwargs):
        self.handle_active()
        super(UserSubscription, self).save(*args, **kwargs)

    def clean(self):
        self.handle_active()
        super().clean()

        if self.subscriber == self.user:
            raise ValidationError("Cannot self-subscribe")

    def handle_active(self):
        if self.active:
            if self.activated_date is None:
                self.activated_date = timezone.now()
                self.deactivated_date = None
        elif self.deactivated_date is None:
            self.deactivated_date = timezone.now()
            self.activated_date = None
