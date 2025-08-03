import secrets

from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone

from blog.services.mailgun_service import MailgunService


class Subscription(models.Model):
    activated_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    active = models.BooleanField(default=True, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    deactivated_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    email = models.EmailField(null=False, blank=False)
    name = models.CharField(validators=[MaxLengthValidator(70)], null=True, blank=True)
    user = models.ForeignKey(to="blog.User", on_delete=models.CASCADE)
    confirmation_token = models.CharField(
        unique=True, max_length=100, null=True, blank=True
    )
    confirmation_token_sent_at = models.DateTimeField(
        auto_now_add=False, null=True, blank=True
    )
    confirmed = models.BooleanField(default=False, null=False)
    confirmed_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)

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
            models.Index(
                fields=["confirmation_token"],
                include=[
                    "confirmation_token_sent_at",
                    "confirmed",
                    "confirmed_at",
                    "id",
                ],
                name="subscription_confirmation_idx",
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

    def generate_confirmation_token(self):
        confirmation_token = secrets.token_urlsafe(64)
        self.confirmation_token = confirmation_token
        self.save()

    def resend_confirmation_email(self):
        if not self.confirmed:
            self.send_confirmation_email()

    def send_confirmation_email(self):
        result = MailgunService.send_subscription_confirmation_email(self)

        if result.status_code == 200:
            self.confirmation_token_sent_at = timezone.now()
            self.save()

    def attempt_confirmation(self):
        self.confirmed = True
        self.confirmed_at = timezone.now()
        self.save()

        return self.confirmed


def post_create_actions(sender, instance, created, **kwargs):
    if created:
        if not instance.confirmed:
            instance.generate_confirmation_token()
            instance.send_confirmation_email()


models.signals.post_save.connect(post_create_actions, sender=Subscription)
