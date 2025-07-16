from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    user = models.ForeignKey(to="blog.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "user")
        verbose_name_plural = "Category"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    def post_count(self):
        return self.posts.filter(draft=False).count()

    def posts(self):
        return self.posts.filter(draft=False)

    def find_by_slug_and_username(slug, username):
        return get_object_or_404(Category, slug=slug, user__username=username)

    def find_list_by_username(username):
        return Category.objects.filter(user__username=username)
