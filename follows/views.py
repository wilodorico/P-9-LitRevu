from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages

from follows.models import UserFollow

User = get_user_model()


class FollowsView(LoginRequiredMixin, View):
    template_name = "follows/follow_home.html"

    def get(self, request):
        followings = UserFollow.objects.get_followings(request.user)
        followers = UserFollow.objects.get_followers(request.user)

        return render(request, self.template_name, {"followings": followings, "followers": followers})


class UnFollowHtmxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        followed_user_id = kwargs["user_id"]
        user_follow = UserFollow.objects.filter(user=request.user, followed_user_id=followed_user_id).first()
        if user_follow:
            user_follow.delete()

        followings = UserFollow.objects.filter(user=request.user)
        messages.success(request, "Vous n'êtes plus abonné à cet utilisateur.")

        return render(request, "follows/includes/following_list.html", {"followings": followings})
