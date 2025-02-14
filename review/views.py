from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from follows.models import UserFollow
from review.forms import ReviewForm, TicketForm
from review.models import Review, Ticket
from review.permissions.edit_access import review_owner_required, ticket_owner_required


class HomeView(LoginRequiredMixin, View):
    template_name = "review/home.html"

    def get(self, request):
        user = request.user

        # Récupérer les utilisateurs suivis
        followed_users = UserFollow.objects.get_followings(user).values_list("followed_user", flat=True)

        # Récupérer les tickets et reviews des utilisateurs suivis + utilisateur lui-même
        users_to_include = list(followed_users) + [user]

        tickets = Ticket.objects.filter(user__in=users_to_include)
        reviews = Review.objects.filter(user__in=users_to_include)

        # Création d'un dictionnaire associant chaque ticket à un booléen indiquant
        # si l'utilisateur a déjà posté une review
        user_reviews = Review.objects.filter(user=user).values_list("ticket_id", flat=True)
        tickets_with_reviews = {ticket.id: ticket.id in user_reviews for ticket in tickets}

        # Fusionner les requêtes et trier par date de création (antéchronologique)
        posts = sorted(list(tickets) + list(reviews), key=lambda post: post.time_created, reverse=True)

        return render(request, self.template_name, {"posts": posts, "tickets_with_reviews": tickets_with_reviews})


class TicketCreateView(LoginRequiredMixin, View):
    template_name = "review/ticket_form.html"

    def get(self, request):
        ticket_form = TicketForm()
        return render(request, self.template_name, {"ticket_form": ticket_form})

    def post(self, request):
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("review:home")


@method_decorator(ticket_owner_required, name="dispatch")
class TicketUpdateView(LoginRequiredMixin, View):
    template_name = "review/ticket_form.html"

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket_form = TicketForm(instance=ticket)
        return render(request, self.template_name, {"ticket_form": ticket_form})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect("review:user_posts")


@method_decorator(ticket_owner_required, name="dispatch")
class TicketDeleteView(LoginRequiredMixin, View):
    template_name = "review/includes/delete_confirm.html"

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        cancel_url = reverse("review:user_posts")
        return render(request, self.template_name, {"object": ticket, "cancel_url": cancel_url})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.delete()
        messages.success(request, "Demande de critique supprimée.")
        return redirect("review:user_posts")


class ReviewCreateView(LoginRequiredMixin, View):
    template_name = "review/review_form.html"

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        review_form = ReviewForm()
        return render(request, self.template_name, {"review_form": review_form, "ticket": ticket})

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


@method_decorator(review_owner_required, name="dispatch")
class ReviewUpdateView(LoginRequiredMixin, View):
    template_name = "review/review_form.html"

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review_form = ReviewForm(instance=review)
        return render(request, self.template_name, {"review_form": review_form, "ticket": review.ticket})

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review_form = ReviewForm(request.POST, instance=review)
        rating_input = int(request.POST.get("rating"))
        if review_form.is_valid():
            form_instance = review_form.save(commit=False)
            form_instance.user = request.user
            form_instance.rating = rating_input
            form_instance.save()
            messages.success(request, ("Commentaire mis à jour !"))
            return redirect("review:user_posts")
        return render(request, self.template_name, {"review_form": review_form, "ticket": review.ticket})


@method_decorator(review_owner_required, name="dispatch")
class ReviewDeleteView(LoginRequiredMixin, View):
    template_name = "review/includes/delete_confirm.html"

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        cancel_url = reverse("review:user_posts")
        return render(request, self.template_name, {"object": review, "cancel_url": cancel_url})

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        messages.success(request, "Commentaire supprimé.")
        return redirect("review:user_posts")


class UserPostsView(LoginRequiredMixin, View):
    template_name = "review/user_posts.html"

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user).select_related("ticket")
        combined_posts = list(chain(tickets, reviews))
        sorted_posts = sorted(combined_posts, key=attrgetter("time_created"), reverse=True)

        return render(request, self.template_name, {"posts": sorted_posts})


class TicketReviewCreateView(View):
    template_name = "review/ticket_review_form.html"

    def get(self, request):
        ticket_form = TicketForm()
        review_form = ReviewForm()
        return render(request, self.template_name, {"ticket_form": ticket_form, "review_form": review_form})

    def post(self, request):
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        rating_input = int(request.POST.get("rating"))
        if ticket_form.is_valid() and review_form.is_valid():
            with transaction.atomic():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.rating = rating_input
                review.save()
                messages.success(request, "Critique publiée !")
            return redirect("review:home")
        return render(request, self.template_name, {"ticket_form": ticket_form, "review_form": review_form})
