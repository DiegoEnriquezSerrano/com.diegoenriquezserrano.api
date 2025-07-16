from django.apps import apps
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save

from .profile import Profile


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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def posts(self):
        return self.post_set.filter(user=self, draft=False).order_by("-id")


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
