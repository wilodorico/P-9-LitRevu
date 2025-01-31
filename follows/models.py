from django.db import models
from django.conf import settings


class UserFollow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user} suit {self.followed_user}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "followed_user"], name="unique_follow")]

    def save(self, *args, **kwargs):
        if self.user == self.followed_user:
            raise ValueError("Vous ne pouvez pas suivre vous-même.")
        super().save(*args, **kwargs)
