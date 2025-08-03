from django.db import models
from django.core.validators import MaxLengthValidator


class Comment(models.Model):
    body = models.TextField(validators=[MaxLengthValidator(500)])
    created_on = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(to="blog.Post", on_delete=models.CASCADE)
    user = models.ForeignKey(to="blog.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Comment"

    def __str__(self):
        return self.post.title + "__" + self.body

    def post_title(self):
        return self.post.title

    def username(self):
        return self.user.username

    def profile(self):
        return self.user.profile
