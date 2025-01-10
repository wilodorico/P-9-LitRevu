from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("inscription/", views.SignupView.as_view(), name="signup"),
    path("connexion/", views.LoginView.as_view(), name="login"),
]
