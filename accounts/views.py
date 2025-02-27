from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from accounts.decorators import user_not_authenticated
from accounts.forms import LoginForm, SignupForm


@method_decorator(user_not_authenticated, name="dispatch")
class SignupView(View):
    template_name = "accounts/signup.html"

    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Votre compte a été créé."))
            return redirect("accounts:login")
        else:
            return render(request, self.template_name, {"form": form})


@method_decorator(user_not_authenticated, name="dispatch")
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
                messages.success(request, ("Vous êtes connecté."))
                return redirect("review:home")
            else:
                form.add_error(None, ("Le nom d'utilisateur ou le mot de passe est incorrect."))
                return render(request, self.template_name, {"form": form})
        else:
            return render(request, self.template_name, {"form": form})


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
