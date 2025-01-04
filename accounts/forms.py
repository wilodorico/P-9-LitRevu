from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm
from .models import User


class SignupForm(AuthUserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        labels = {
            "username": "Nom d'utilisateur",
            "password1": "Mot de passe",
            "password2": "Confirmation du mot de passe",
        }
