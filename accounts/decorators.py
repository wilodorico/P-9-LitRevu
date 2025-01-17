from django.shortcuts import redirect
from functools import wraps


def user_not_authenticated(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("review:home")
        return function(request, *args, **kwargs)

    return wrap
