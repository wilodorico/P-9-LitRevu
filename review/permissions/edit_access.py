from functools import wraps
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from review.models import Review, Ticket


def _is_ticket_owner(user, ticket_id):
    """
    Vérifie si l'utilisateur est le propriétaire du ticket.
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return user.is_authenticated and ticket.user == user


def ticket_owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        if not _is_ticket_owner(request.user, ticket_id):
            raise PermissionDenied("Vous n'êtes pas autorisé à accéder à cette page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def _is_review_owner(user, review_id):
    """
    Vérifie si l'utilisateur est le propriétaire de la review.
    """
    review = get_object_or_404(Review, pk=review_id)
    return user.is_authenticated and review.user == user


def review_owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        review_id = kwargs.get("review_id")
        if not _is_review_owner(request.user, review_id):
            raise PermissionDenied("Vous n'êtes pas autorisé à accéder à cette page.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
