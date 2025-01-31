from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from follows.models import UserFollow


class FollowsView(LoginRequiredMixin, View):
    template_name = "follows/follow_home.html"

    def get(self, request):
        followings = UserFollow.objects.get_followings(request.user)
        followers = UserFollow.objects.get_followers(request.user)

        return render(request, self.template_name, {"followings": followings, "followers": followers})
