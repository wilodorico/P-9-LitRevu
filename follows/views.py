from django.shortcuts import render
from django.views import View


class FollowsView(View):
    template_name = "follows/follow_home.html"

    def get(self, request):
        return render(request, self.template_name)
