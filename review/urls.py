from django.urls import path

from review import views


app_name = "review"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("ticket/create/", views.TicketCreateView.as_view(), name="ticket_create"),
]
