from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone


class Subscription(models.Model):
    activated_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    active = models.BooleanField(default=True, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    deactivated_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    name = models.CharField(validators=[MaxLengthValidator(70)], null=True, blank=True)
    user = models.ForeignKey(to="blog.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-activated_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "email"], name="unique_subscriptions"
            ),
            models.CheckConstraint(
                condition=models.Q(activated_date__isnull=False)
                | models.Q(deactivated_date__isnull=False),
                name="prevent_subscriptions_deactivated_and_activated_null",
            ),
            models.CheckConstraint(
                condition=models.Q(activated_date__isnull=True)
                | models.Q(deactivated_date__isnull=True),
                name="prevent_subscriptions_deactivated_and_activated_present",
            ),
            models.CheckConstraint(
                condition=models.Q(active=True, activated_date__isnull=False)
                | models.Q(active=False, deactivated_date__isnull=False),
                name="prevent_subscriptions_active_and_activated_date_null",
            ),
        ]
        indexes = [
            models.Index(
                fields=["user", "email"],
                include=["active"],
                name="subscription_email_idx",
            ),
        ]

    def __str__(self):
        return f"{self.email} to {self.user.username}"

    def save(self, *args, **kwargs):
        self.handle_active()
        super(Subscription, self).save(*args, **kwargs)

    def clean(self):
        self.handle_active()
        super().clean()

        if self.email == self.user.email:
            raise ValidationError("Cannot self-subscribe")

    def handle_active(self):
        if self.active:
            if self.activated_date is None:
                self.activated_date = timezone.now()
                self.deactivated_date = None
        elif self.deactivated_date is None:
            self.deactivated_date = timezone.now()
            self.activated_date = None
