from django.db import models
from django.shortcuts import get_object_or_404

from .post import Post


class Bookmark(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(to="blog.Post", on_delete=models.CASCADE)
    user = models.ForeignKey(to="blog.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Bookmark"

    def __str__(self):
        return self.post.title

    def create_or_delete(user, post_id):
        post = get_object_or_404(Post, id=post_id)

        if Bookmark.objects.filter(user=user, post=post).exists():
            get_object_or_404(Bookmark, post=post, user=user).delete()

            return "deleted"
        else:
            Bookmark.objects.create(user=user, post=post)

            return "created"
