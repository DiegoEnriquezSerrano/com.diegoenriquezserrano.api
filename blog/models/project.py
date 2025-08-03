from django.contrib.postgres import fields
from django.core.validators import MaxLengthValidator
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


class Project(models.Model):
    STATUS = (("completed", "completed"), ("ongoing", "ongoing"))

    body = models.TextField(null=True, blank=True)
    cover_image_url = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(
        validators=[MaxLengthValidator(200)], null=False, blank=False
    )
    finished_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=False, null=False, blank=False)
    status = models.CharField(choices=STATUS)
    title = models.CharField(max_length=70)
    tools = fields.ArrayField(models.CharField(max_length=25), blank=True, null=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    user = models.OneToOneField(to="blog.User", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "slug"], name="unique_user_projects"
            ),
            models.CheckConstraint(
                condition=models.Q(status__exact="ongoing", finished_at__isnull=True)
                | models.Q(finished_at__isnull=False),
                name="ensure_finished_at_for_completed_projects",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def find_by_slug_and_username(slug, username):
        return get_object_or_404(Project, slug=slug, user__username=username)

    def find_list_by_username(username):
        return Project.objects.filter(user__username=username)

    def profile(self):
        return self.user.profile
