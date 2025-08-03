from django.db import models
from django.core.validators import MaxLengthValidator
from django.shortcuts import get_object_or_404
from django.utils.text import slugify


class Post(models.Model):
    body = models.TextField()
    categories = models.ManyToManyField(to="blog.Category", related_name="posts")
    cover_image_url = models.URLField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(validators=[MaxLengthValidator(200)])
    draft = models.BooleanField(default=False)
    excerpt = models.TextField(validators=[MaxLengthValidator(200)])
    featured = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        to="blog.User", blank=True, related_name="likes_user"
    )
    slug = models.SlugField(null=True, blank=True)
    title = models.CharField(max_length=70, unique=True)
    user = models.ForeignKey(to="blog.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]
        unique_together = ("slug", "user")
        verbose_name_plural = "Post"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            self.slug = slugify(self.title)
        if should_feature_post(self):
            self.featured = True
        super(Post, self).save(*args, **kwargs)

    def comments(self):
        return self.comment_set.filter(post=self).order_by("-id")

    def profile(self):
        return self.user.profile

    def find_by_slug_and_username(slug, username):
        return get_object_or_404(Post, slug=slug, user__username=username)

    def find_list_by_username(username):
        return Post.objects.filter(user__username=username, draft=False)

    def toggle_like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)

            return "unliked"
        else:
            self.likes.add(user)

            return "liked"


def should_feature_post(post):
    return (
        not post.draft
        and Post.objects.filter(featured=True, draft=False, user=post.user).count() == 0
    )
