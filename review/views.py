from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib import messages

from review.forms import ReviewForm, TicketForm
from review.models import Ticket
from review.permissions.edit_access import ticket_owner_required


class HomeView(LoginRequiredMixin, View):
    template_name = "review/home.html"

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).order_by("-time_created")
        return render(request, self.template_name, {"tickets": tickets})


class TicketCreateView(LoginRequiredMixin, View):
    template_name = "review/ticket_form.html"

    def get(self, request):
        form = TicketForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect("review:home")


@method_decorator(ticket_owner_required, name="dispatch")
class TicketUpdateView(LoginRequiredMixin, View):
    template_name = "review/ticket_form.html"

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = TicketForm(instance=ticket)
        return render(request, self.template_name, {"form": form})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect("review:home")


@method_decorator(ticket_owner_required, name="dispatch")
class TicketDeleteView(LoginRequiredMixin, View):
    template_name = "review/ticket_delete_confirm.html"

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        return render(request, self.template_name, {"ticket": ticket})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.delete()
        messages.success(request, "Demande de critique supprimée.")
        return redirect("review:home")


class ReviewCreateView(LoginRequiredMixin, View):
    template_name = "review/review_form.html"

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = ReviewForm()
        return render(request, self.template_name, {"form": form, "ticket": ticket})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = ReviewForm(request.POST)
        rating_input = int(request.POST.get("rating"))

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = request.user
            form_instance.ticket = ticket
            form_instance.rating = rating_input
            form_instance.save()
            messages.success(request, ("Merci pour votre commentaire !"))
            return redirect("review:home")

        return render(request, self.template_name, {"form": form, "ticket": ticket})
