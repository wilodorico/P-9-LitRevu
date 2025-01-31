from django.urls import path

from follows import views

app_name = "follows"

urlpatterns = [
    path("", views.FollowsView.as_view(), name="follow_home"),
]
