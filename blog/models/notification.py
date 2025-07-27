from django.db import models


class Notification(models.Model):
    TYPE = (("like", "like"), ("comment", "comment"))

    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(to="blog.Post", on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    type = models.CharField(choices=TYPE)
    user = models.ForeignKey(to="blog.User", on_delete=models.CASCADE)
    comment = models.ForeignKey(
        to="blog.Comment", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Notification"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(type__exact="comment", comment__isnull=False)
                | models.Q(comment__isnull=True),
                name="ensure_notification_type_comment_has_comment",
            ),
        ]

    def __str__(self):
        if self.post:
            return f"{self.post.title} - {self.type}"
        else:
            return "Notification"

    def profile(self):
        return self.user.profile
