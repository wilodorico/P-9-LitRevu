from functools import wraps

from django.shortcuts import redirect


def user_not_authenticated(function):
    """
    Decorator for views that checks that the user is not authenticated.
    If the user is authenticated, they are redirected to the home page of the review app.
    Otherwise, the original view function is called.
    Args:
        function (function): The view function to be decorated.
    Returns:
        function: The wrapped view function.
    """

    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("review:home")
        return function(request, *args, **kwargs)

    return wrap
