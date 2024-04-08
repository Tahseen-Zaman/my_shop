from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle, Travel, Seat, Ticket
from .forms import BookTicketForm, SearchForm


def home(request):
    travel = Travel.objects.all()
    return render(request, "tickets/home.html", {"travels": travel})

def travel(request):
    travel = Travel.objects.all()
    return render(request, "tickets/travel.html", {"travels": travel})


from datetime import datetime, time

start_time = time.min  # Start time is midnight
end_time = time.max  # End time is 23:59:59.999999


def search_travels(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            origin = form.cleaned_data["origin"]
            destination = form.cleaned_data["destination"]
            departure_time = form.cleaned_data["departure_time"]
            date_obj = departure_time
            travels = Travel.objects.filter(
                origin=origin,
                destination=destination,
            ).filter(
                departure_time__range=(
                    datetime.combine(date_obj, start_time),
                    datetime.combine(date_obj, end_time),
                )
            )
            return render(request, "tickets/search_results.html", {"travels": travels})
    else:
        form = SearchForm()
    return render(request, "tickets/search_travels.html", {"form": form})


def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    available_seats = vehicle.get_available_seats()
    return render(
        request,
        "tickets/vehicle_detail.html",
        {"vehicle": vehicle, "available_seats": available_seats},
    )

@login_required
def book_ticket(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id)
    print(travel_id)

    if request.method == "POST":
        form = BookTicketForm(request.POST, my_param =travel_id )
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.travel_info = travel
            seat_numbers = form.cleaned_data["seat_numbers"]
            if ticket.book_seats(seat_numbers):
                messages.success(request, "Your ticket has been booked successfully!")
                return redirect("tickets:ticket_detail", ticket_id=ticket.id)
            else:
                messages.error(
                    request, "Some or all of the seats you selected are not available."
                )
    else:
        form = BookTicketForm(my_param=travel_id)

    context = {"travel": travel, "form": form}
    return render(request, "tickets/book_ticket.html", context)

def ticket_detail(request, ticket_id ):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})

def travel_detail(request, travel_id ):
    travel = get_object_or_404(Travel, id=travel_id)
    return render(request, "tickets/travel_detail.html", {"travel": travel})