from django.db import models


class Notification(models.Model):
    TYPE = (("like", "like"), ("comment", "comment"))

    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(to="blog.Post", on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    type = models.CharField(choices=TYPE)
    user = models.ForeignKey(to="blog.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Notification"

    def __str__(self):
        if self.post:
            return f"{self.post.title} - {self.type}"
        else:
            return "Notification"
