from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hotel, Room, Booking
from .forms import BookingForm, SearchHotelForm, RoomSearchForm
from django.db.models import Q
from django.db.models import Sum

def home(request):
    hotels = Hotel.objects.all()
    return render(request, "hotels/home.html", {"hotels": hotels})


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    # rooms = get_object_or_404(Room, hotel=hotel)
    rooms = Room.objects.filter(hotel=hotel)
    return render(request, "hotels/hotel_detail.html", {"hotel": hotel, "rooms": rooms})


def room_detail(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room = get_object_or_404(Room, pk=room_id, hotel=hotel)
    return render(request, "hotels/room_detail.html", {"hotel": hotel, "room": room})


def search_available_hotels(request):
    if request.method == "POST":
        form = SearchHotelForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data.get("location")
            hotel_type = form.cleaned_data.get("hotel_type", None)
            available_hotels = Hotel.objects.filter(
                location=location)
            if hotel_type: 
                available_hotels = available_hotels.filter(hotel_type=hotel_type).distinct()
            context = {
                "location": location,
                "hotels": available_hotels,
            }
            return render(request, "hotels/search_results.html", context)
    else:
        form = SearchHotelForm()

    context = {"form": form}
    return render(request, "hotels/search_hotels.html", context)

@login_required
def book_room(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    if request.method == "POST":
        form = BookingForm(hotel, request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data["check_in_date"]
            check_out_date = form.cleaned_data["check_out_date"]
            num_guests = form.cleaned_data["num_guests"]
            rooms = form.cleaned_data["room"]
            total_price = 0 
            for room in rooms:
                total_price += (
                    room.price * (check_out_date - check_in_date).days * num_guests
                )
            booking = Booking.objects.create(
                user=request.user,
                hotel=hotel,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                num_guests=num_guests,
                total_price=total_price,
            )
            booking.room.set(rooms)
            booking.save()
            messages.success(
                request,
                f"Room {room.room_number} at {hotel.hotel_name} has been booked successfully!",
            )
            return redirect("hotels:booking_detail", booking_id=booking.booking_id)
    else:
        form = BookingForm(hotel)
    return render(request, "hotels/book_room.html", {"hotel": hotel, "form": form})



def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    overstay_charge = booking.calculate_overstay_charge()
    return render(
        request,
        "hotels/booking_detail.html",
        {"booking": booking, "overstay_charge": overstay_charge},
    )


def search_available_room(request, hotel_id):
    hotel = Hotel.objects.get(hotel_id=hotel_id)
    if request.method == 'POST':
        form = RoomSearchForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data['room_type']
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            available_rooms = Room.objects.filter(hotel=hotel, room_type=room_type, max_capacity__gte=form.cleaned_data['num_guests'])
            for room in available_rooms:
                if not room.is_available(check_in, check_out):
                    available_rooms = available_rooms.exclude(room_id=room.room_id)
            return render(request, 'hotels/available_rooms.html', {'hotel': hotel, 'available_rooms': available_rooms})
    else:
        form = RoomSearchForm(hotel_id)
    return render(request, 'hotels/room_search.html', {'form': form})

def view_voucher(request):
#     ver_dict = {

#   "check_in": "2:00 PM, Saturday, 30 Sep, 2023",
#   "check_out": "12:00 PM, Sunday, 01 Oct, 2023",
#   "hotel_fax": "N/A",
#   "hotel_name": "Hotel Sarina",
#   "rate_class": "Refundable",
#   "vat_number": "",
#   "addons_list": [],
#   "hotel_email": "N/A",
#   "hotel_image": "http://photos.hotelbeds.com/giata/original/41/411038/411038a_hb_a_010.jpg",
#   "hotel_phone": "N/A",
#   "gz_reference": "HB2204030001",
#   "hotel_rating": "5",
#   "hotel_address": "Plot #27, Road #17, Banani C/A, Dhaka 1213, Banani, 4, BD",
#   "optional_fees": "Coke Tk40",
#   "supplier_name": "Hotelbeds",
#   "mandatory_fees": "Breakfast Tk50",
#   "payable_amount": "BDT 15,193",
#   "hotel_reference": "448-4988",
#   "primary_contact": "tanvir palash",
#   "is_expedia_hotel": False,
#   "reservation_date": "Sun, 03 Apr, 2022",
#   "is_gozayaan_hotel": True,
#   "room_cancel_policy": [
#     {
#       "room_name": "DOUBLE DELUXE",
#       "room_policy": {
#         "1": [
#           "Free cancellation upto YYYY-MM-DD.",
#           "Cancellation charge BDT 4000 from YYYY-MM-DD."
#         ]
#       }
#     },
#     {
#       "room_name": "DOUBLE DELUXE",
#       "room_policy": {
#         "1": [
#           "Free cancellation upto YYYY-MM-DD.",
#           "Cancellation charge BDT 4000 from YYYY-MM-DD."
#         ]
#       }
#     },
#     {
#       "room_name": "DOUBLE DELUXE",
#       "room_policy": {
#         "1": [
#           "Free cancellation upto YYYY-MM-DD.",
#           "Cancellation charge BDT 4000 from YYYY-MM-DD."
#         ]
#       }
#     },
#     {
#       "room_name": "DOUBLE DELUXE",
#       "room_policy": {
#         "1": [
#           "Free cancellation upto YYYY-MM-DD.",
#           "Cancellation charge BDT 4000 from YYYY-MM-DD."
#         ]
#       }
#     }
#   ],
#   "room_voucher_details": [
#     {
#       "adult": "1",
#       "board": "Bed and breakfast",
#       "child": "2 (Age 5, Age 7)",
#       "remarks": " .  Check-in hour -12:00.Car park YES (with additional debit notes).Due to the pandemic, many accommodation and service providers may implement processes and policies to help protect the safety of all of us. This may result in the unavailability or changes in certain services and amenities that are normally available from them. More info here https://cutt.ly/MT8BJcv (15/05/2020-30/06/2022) ",
#       "included": [
#         "Free WIFI",
#         "Breakfast"
#       ],
#       "room_name": "DOUBLE DELUXE",
#       "customer_name": "tanvir palash"
#     }
#   ],
#   "check_in_instructions": "Just check in",
#   "check_out_instructions": "Just check out",
#     "hotel_booking_id": "HB2204030001",
#       "nights": 2,
#                   "primary_contact_phone": "primary_contact_phone",
#             "primary_contact_email": "primary_contact_email",
# "room_details": [
#     {
#         "room_name": "Junior Suite Sea View",
#         "paxes": [
#             {
#                 "name": "Mesba Ul Azim",
#                 "type": "AD"
#             }, 
#             {
#                 "name": "Tasfia Khan", 
#                 "type": "CH"
#             }
#         ],
#         "plan": "Bed & Breakfast (Non-Refundable)"
#     },
#     {
#         "room_name": "Junior Suite View",
#         "paxes": [
#             {
#                 "name": "Ibrahim Imran",
#                 "type": "AD"
#             }, 
#             {
#                 "name": "Laily Akhter", 
#                 "type": "CH"
#             }
#         ],
#         "plan": "Bed & Breakfast (Refundable)"
#     },
#     {
#         "room_name": "Suite Sea View",
#         "paxes": [
#             {
#                 "name": "Mesbzim",
#                 "type": "AD"
#             }, 
#             {
#                 "name": "Tasfhan", 
#                 "type": "AD"
#             }
#         ],
#         "plan": "Bed & Breakfast (Refundable)"
#     },
#     {
#         "room_name": "Junior Suite Sea",
#         "paxes": [
#             {
#                 "name": "Azim",
#                 "type": "AD"
#             }, 
#             {
#                 "name": "Khan", 
#                 "type": "AD"
#             }
#         ],
#         "plan": "Bed & Breakfast (Refundable)"
#     }
# ],
#             "pet_policy": "Not Allowed",
#                         "house_rules": "house_rules",
#                         "is_bd_region": True,
#                         "is_expedia_hotel": True,
#                         "check_in_instruction": "Pay Hotel boy 500 taka",
#                         "mandatory_fees": "505.50",
#                         "child_policy": "Only year 5 Allowed",
#                         "map_hotel":"https://maps.app.goo.gl/YrpxNppK3rZ3ATGC9"
# }
    ver_dict={
        'name': "Tahseen Zaman",
        'booking_id': "123456",
        'region': "BD",
        'amount': 'BDT 1,500.00',
            }
    return render(
        request,
        "hotels/payment-confirmation-v2.html",
        ver_dict,
    )
