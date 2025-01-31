from django.db import models
from django.conf import settings


class UserFollowManager(models.Manager):
    def get_followings(self, user):
        return self.filter(user=user).select_related("followed_user")

    def get_followers(self, user):
        return self.filter(followed_user=user).select_related("user")


class UserFollow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")

    objects = UserFollowManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "followed_user"], name="unique_follow")]

    def __str__(self):
        return f"{self.user} suit {self.followed_user}"

    def save(self, *args, **kwargs):
        if self.user == self.followed_user:
            raise ValueError("Vous ne pouvez pas suivre vous-même.")
        super().save(*args, **kwargs)
