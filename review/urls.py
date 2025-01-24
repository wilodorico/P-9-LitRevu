from django.urls import path

from review import views


app_name = "review"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("ticket/créer/", views.TicketCreateView.as_view(), name="ticket_create"),
    path("ticket/<int:ticket_id>/modifier/", views.TicketUpdateView.as_view(), name="ticket_update"),
    path("ticket/<int:ticket_id>/supprimer/", views.TicketDeleteView.as_view(), name="ticket_delete"),
    path("ticket/<int:ticket_id>/critique/créer/", views.ReviewCreateView.as_view(), name="review_create"),
]
