from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

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

        return render(request, "follows/includes/hx_following_success.html", {"followings": followings})


def follow_user(request):
    followings = UserFollow.objects.filter(user=request.user)
    username = request.POST.get("username")

    if not username:
        messages.info(request, "Veuillez saisir un nom d'utilisateur.")
        return render(request, "follows/includes/hx_following_success.html", {"followings": followings})

    user_to_follow = get_object_or_404(User, username=username)

    if UserFollow.objects.filter(user=request.user, followed_user=user_to_follow).exists():
        messages.info(request, f"Vous êtes déjà abonné à {user_to_follow}.")
        return render(request, "follows/includes/hx_following_success.html", {"followings": followings})

    if request.user != user_to_follow:
        UserFollow.objects.get_or_create(user=request.user, followed_user=user_to_follow)
        messages.success(request, "Vous êtes maintenant abonné à cet utilisateur.")

    return render(request, "follows/includes/hx_following_success.html", {"followings": followings})


def search_users(request):
    query = request.GET.get("search", "").strip()
    if not query:
        return HttpResponse("")

    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    return render(request, "follows/includes/search_results.html", {"users": users})
