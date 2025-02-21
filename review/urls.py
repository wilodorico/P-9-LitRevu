from django.urls import path

from review import views


app_name = "review"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("ticket/créer/", views.TicketCreateView.as_view(), name="ticket_create"),
    path("ticket/<int:ticket_id>/modifier/", views.TicketUpdateView.as_view(), name="ticket_update"),
    path("ticket/<int:ticket_id>/supprimer/", views.TicketDeleteView.as_view(), name="ticket_delete"),
    path("ticket/<int:ticket_id>/critique/créer/", views.ReviewCreateView.as_view(), name="review_create"),
    path("review/<int:review_id>/critique/modifier/", views.ReviewUpdateView.as_view(), name="review_update"),
    path("review/<int:review_id>/supprimer/", views.ReviewDeleteView.as_view(), name="review_delete"),
    path("ticket-review/créer/", views.TicketReviewCreateView.as_view(), name="ticket_review_create"),
    path("my_posts/", views.UserPostsView.as_view(), name="user_posts"),
]
