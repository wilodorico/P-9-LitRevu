from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from review.forms import TicketForm
from review.models import Ticket


class HomeView(LoginRequiredMixin, View):
    template_name = "review/home.html"

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
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
