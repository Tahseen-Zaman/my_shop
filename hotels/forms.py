from django import forms
from .models import Hotel, Booking, Room
from django.db.models import Q
from datetime import date

class SearchHotelForm(forms.Form):
    location = forms.ChoiceField(choices=Hotel.CITY_CHOICES)
    hotel_type = forms.ChoiceField(choices=Hotel.HOTEL_TYPES)


class BookingForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    num_guests = forms.IntegerField(min_value=1)
    room = forms.ModelMultipleChoiceField(
        queryset=Room.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, hotel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hotel_id = hotel_id
        self.fields['room'].queryset = self.get_available_rooms()

    def get_available_rooms(self):
        # Get the available rooms for the selected hotel and dates
        bookings = Booking.objects.filter(
            hotel_id=self.hotel_id,
            check_out_date__gt=date.today()
        ).prefetch_related('room')
        booked_rooms = set(room.room_id for booking in bookings for room in booking.room.all())
        available_rooms = Room.objects.filter(hotel_id=self.hotel_id).exclude(room_id__in=booked_rooms)
        return available_rooms

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        room = cleaned_data.get('room')
        if check_in_date and check_out_date and room:
            # Check if the selected room is available for the specified dates
            bookings = Booking.objects.filter(
                hotel_id=self.hotel_id,
                room__in=room,
                check_out_date__gt=check_in_date,
                check_in_date__lt=check_out_date
            )
            if bookings.exists():
                raise forms.ValidationError('This room is not available for the selected dates.')
        return cleaned_data

class RoomSearchForm(forms.Form):
    room_type = forms.ChoiceField(choices=Room.ROOM_TYPES)
    check_in = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, hotel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hotel_id = hotel_id

    def clean(self):
        cleaned_data = super().clean()
        room_type = cleaned_data.get('room_type')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        if room_type and check_in and check_out:
            # Check if any room of the specified type is available
            rooms = Room.objects.filter(hotel_id=self.hotel_id, room_type=room_type)
            if not rooms.exists():
                raise forms.ValidationError("No rooms of this type are available.")
            # Check if the selected check-in date is after the check-out date
        if check_in >= check_out:
            raise forms.ValidationError("Check-in date must be before check-out date.")
        return cleaned_data
