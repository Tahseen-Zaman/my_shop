from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.home, name="home"),
    path("travel/", views.travel, name="travel"),
    path("search_travels/", views.search_travels, name="search_travels"),
    path("travels/<int:travel_id>/book/", views.book_ticket, name="book_travel"),
    path("vehicles/<int:vehicle_id>/", views.vehicle_detail, name="vehicle_detail"),
    path("ticket/<int:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    
    path("travel/<int:travel_id>/", views.travel_detail, name="travel_detail"),
]
