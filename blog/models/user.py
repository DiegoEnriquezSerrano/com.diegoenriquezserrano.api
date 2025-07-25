import secrets

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from .profile import Profile
from .user_subscription import UserSubscription

from blog.services.email_service import EmailService


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        unique=True,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r"^[\w.~-]*$",
                message="Only alphanumeric characters (0-9, A-Z, a-z), hyphens (-) and/or underscores (_) allowed in username",
                code="invalid_registration",
            )
        ],
    )
    confirmation_token = models.CharField(
        unique=True, max_length=100, null=True, blank=True
    )
    confirmation_token_sent_at = models.DateTimeField(
        auto_now_add=False, null=True, blank=True
    )
    confirmed = models.BooleanField(default=False, null=False)
    confirmed_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    subscribers = models.ManyToManyField(
        to="self",
        through="UserSubscription",
        related_name="subscribed",
        symmetrical=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        indexes = [
            models.Index(
                fields=["confirmation_token"],
                include=[
                    "confirmation_token_sent_at",
                    "confirmed",
                    "confirmed_at",
                    "id",
                ],
                name="users_confirmation_token_idx",
            ),
            models.Index(
                fields=["confirmed", "id"],
                include=[
                    "email",
                    "username",
                ],
                name="confirmed_users_idx",
            ),
        ]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def posts(self):
        return self.post_set.filter(user=self, draft=False).order_by("-id")

    def total_active_subscribers(self):
        return UserSubscription.objects.filter(user=self.id, active=True).count()

    def total_active_subscribed(self):
        return UserSubscription.objects.filter(subscriber=self.id, active=True).count()

    def generate_confirmation_token(self):
        confirmation_token = secrets.token_urlsafe(64)
        self.confirmation_token = confirmation_token
        self.save()

    def resend_confirmation_email(self):
        if not self.confirmed:
            self.send_confirmation_email()

    def send_confirmation_email(self):
        result = EmailService.send_confirmation_email(self)

        if result["Message"] == "OK":
            self.confirmation_token_sent_at = timezone.now()
            self.save()

    def attempt_confirmation(self):
        self.confirmed = True
        self.confirmed_at = timezone.now()
        self.save()

        return self.confirmed


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        if not instance.confirmed:
            instance.generate_confirmation_token()
            instance.send_confirmation_email()


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
