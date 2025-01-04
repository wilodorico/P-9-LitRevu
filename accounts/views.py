from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from accounts.forms import SignupForm


class SignupView(View):
    template_name = "accounts/signup.html"

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("User created")
        else:
            return render(request, self.template_name, {"form": form})
