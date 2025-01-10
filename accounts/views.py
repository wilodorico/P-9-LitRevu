from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, authenticate

from accounts.forms import LoginForm, SignupForm


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


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return HttpResponse("User logged in")
        else:
            return render(request, self.template_name, {"form": form})
