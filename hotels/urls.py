from django.urls import path

from . import views

app_name = "hotels"

urlpatterns = [
    path("hotel", views.home, name="home"),
    path("hotels/<str:hotel_id>/", views.hotel_detail, name="hotel_detail"),
    path("search_hotel/", views.search_available_hotels, name="search_hotel"),
    path("hotels/<str:hotel_id>/search_room/", views.search_available_room, name="search_available_room"),
    path(
        "hotels/<int:hotel_id>/room/<int:room_id>/",
        views.room_detail,
        name="room_detail",
    ),
    path("hotels/book/<str:hotel_id>/", views.book_room, name="book_room"),
    path("booking/<str:booking_id>/", views.booking_detail, name="booking_detail"),
    path("view_voucher/", views.view_voucher, name="view_voucher"),
]
