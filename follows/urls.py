from django.urls import path

from follows import views

app_name = "follows"

urlpatterns = [
    path("", views.FollowsView.as_view(), name="follow_home"),
    path("unfollow/<int:user_id>", views.UnFollowHtmxView.as_view(), name="unfollow"),
    path("follow/", views.follow_user, name="follow"),
    path("search-users/", views.search_users, name="search_users"),
]
