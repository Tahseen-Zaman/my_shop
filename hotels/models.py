from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime, timedelta
from users.models import Payment
# Create your models here.


class Booking(models.Model):
    booking_id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(
        "Hotel", on_delete=models.CASCADE, related_name="bookings_hotel"
    )
    room = models.ManyToManyField(
        "Room", related_name="bookings_room"
    )
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment,null=True,blank=True, on_delete=models.SET_NULL, related_name="payment_booking")

    def __str__(self):
        return f"{self.user.username}'s booking for hotel {self.hotel.hotel_name}"

    def book_room(self, room):
        if self.is_room_available(room):
            room.book(self.check_in_date, self.check_out_date)
            self.rooms.add(room)
            self.save()
            return True
        else:
            return False

    def calculate_overstay_charge(self):
        check_out = datetime.combine(self.check_out_date, datetime.min.time())
        actual_check_out = datetime.now()
        if actual_check_out > check_out:
            overstay_days = (actual_check_out - check_out).days
            overstay_charge = self.hotel.overstay_rate * overstay_days
            return overstay_charge
        else:
            return 0


class Hotel(models.Model):
    hotel_id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    HOTEL_TYPES = [
        ("budget", "Budget"),
        ("mid-range", "Mid-Range"),
        ("luxury", "Luxury"),
        ("resort", "Resort"),
    ]
    DHAKA = "Dhaka"
    CHITTAGONG = "Chittagong"
    SYLHET = "Sylhet"
    KHULNA = "Khulna"
    BARISAL = "Barisal"

    CITY_CHOICES = [
        (DHAKA, "Dhaka"),
        (CHITTAGONG, "Chittagong"),
        (SYLHET, "Sylhet"),
        (KHULNA, "Khulna"),
        (BARISAL, "Barisal"),
    ]
    hotel_type = models.CharField(max_length=50, choices=HOTEL_TYPES, default="budget")
    hotel_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, choices=CITY_CHOICES)
    overstay_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.hotel_name


class Room(models.Model):
    room_id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    ROOM_TYPES = [
        ("SINGLE", "Single"),
        ("DOUBLE", "Double"),
        ("TWIN", "Twin"),
        ("FAMILY", "Family"),
    ]
    room_number = models.CharField(max_length=10)
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="rooms_hotel"
    )
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Room {self.room_number} at {self.hotel.hotel_name}"

    def is_available(self, check_in, check_out):
        bookings = Booking.objects.filter(hotel=self.hotel)
        for booking in bookings:
            if booking.check_in_date < check_out and booking.check_out_date > check_in:
                rooms = booking.rooms.all()
                if self in rooms:
                    return False
        return True

    def book(self, user, num_guests, check_in, check_out):
        availability = self.is_available(check_in, check_out)
        if availability:
            booking = Booking.objects.create(
                user=user,
                hotel=self.hotel,
                check_in_date=check_in,
                check_out_date=check_out,
                num_guests=num_guests,
                total_price=self.price,
            )
            booking.rooms.add(self)
            booking.save()
            return True
        else:
            return False
