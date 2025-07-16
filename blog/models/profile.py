from django.db import models


class Profile(models.Model):
    author = models.BooleanField(default=False)
    bio = models.CharField(max_length=200, null=True, blank=True)
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