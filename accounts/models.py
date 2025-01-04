from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Model default user"""

    pass

    def __str__(self):
        return self.username
