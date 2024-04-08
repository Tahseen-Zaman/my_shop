from django.db import models
from django.contrib.auth.models import User
import uuid
from users.models import Payment

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ("bus", "Bus"),
        ("train", "Train"),
        ("flight", "Flight"),
    ]
    vehicle_number = models.CharField(max_length=50, unique=True)
    body_manufacturer = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.type:} {self.vehicle_number:}"

    def get_available_seats(self):
        booked_seats = Ticket.objects.filter(travel_info__vehicle=self).values_list(
            "seats", flat=True
        )
        available_seats = Seat.objects.exclude(number__in=booked_seats)
        return available_seats


class Travel(models.Model):
    CITIES_BANGLADESH = [
        ("Dhaka", "Dhaka"),
        ("Chittagong", "Chittagong"),
        ("Sylhet", "Sylhet"),
        ("Khulna", "Khulna"),
        ("Rajshahi", "Rajshahi"),
        ("Barisal", "Barisal"),
        ("Rangpur", "Rangpur"),
        ("Comilla", "Comilla"),
        ("Narayanganj", "Narayanganj"),
        ("Jessore", "Jessore"),
        ("Savar", "Savar"),
        ("Mymensingh", "Mymensingh"),
        ("Tangail", "Tangail"),
        ("Gazipur", "Gazipur"),
        ("Bogra", "Bogra"),
        ("Nawabganj", "Nawabganj"),
        ("Narsingdi", "Narsingdi"),
        ("Joypurhat", "Joypurhat"),
        ("Saidpur", "Saidpur"),
        ("Sirajganj", "Sirajganj"),
    ]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    origin = models.CharField(
        max_length=100, choices=CITIES_BANGLADESH, default="Dhaka"
    )
    destination = models.CharField(max_length=100, choices=CITIES_BANGLADESH)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    def __str__(self):
        return f"{self.vehicle} - {self.origin} to {self.destination} "


class Seat(models.Model):
    SEAT_TYPES = [
        ("standard", "Standard"),
        ("luxury", "Luxury"),
        ("sleeper", "Sleeper"),
    ]

    vehicle = models.ForeignKey(
        Travel, on_delete=models.CASCADE, related_name="seats_vehicle"
    )
    number = models.CharField(max_length=3)
    type = models.CharField(max_length=10, choices=SEAT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.vehicle}  {self.number} ({self.type})"


class Ticket(models.Model):
    ticket_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tickets_user"
    )
    seats = models.ManyToManyField(Seat, related_name="tickets_seat")
    travel_info = models.ForeignKey(
        Travel, on_delete=models.CASCADE, related_name="tickets_travel"
    )
    num_passengers = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment,null=True,blank=True, on_delete=models.SET_NULL, related_name="payment_ticket")


    def __str__(self):
        return f"{self.user.username}'s ticket for {self.travel_info.vehicle} ({self.travel_info.origin} to {self.travel_info.destination})"

    def book_seats(self, seats):
        for seat in seats:
            seat.is_available = False
            seat.save()
        self.num_passengers = len(seats)
        self.total_price = sum(seat.price for seat in seats)
        self.save()
        self.seats.set(seats)
        return True

