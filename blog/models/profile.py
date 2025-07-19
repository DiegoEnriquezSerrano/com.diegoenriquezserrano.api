from django.db import models
from django.core.validators import MaxLengthValidator


class Profile(models.Model):
    bio = models.TextField(null=True, blank=True)
    description = models.TextField(
        validators=[MaxLengthValidator(200)], null=True, blank=True
    )
    display_name = models.CharField(
        validators=[MaxLengthValidator(70)], null=True, blank=True
    )
    image = models.URLField(max_length=200, null=True, blank=True)
    banner = models.URLField(max_length=200, null=True, blank=True)
    bluesky = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    mastodon = models.CharField(max_length=100, null=True, blank=True)
    twitch = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(to="blog.User", on_delete=models.CASCADE)
    youtube = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def username(self):
        return self.user.username
