from django import forms
from django.contrib.auth.models import User
from .models import Ticket, Travel, Seat

from django import forms
from django.shortcuts import get_object_or_404
from django.forms.widgets import CheckboxSelectMultiple


class BookTicketForm(forms.ModelForm):
    seat_numbers = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple,
        label="Select seats",
    )

    def __init__(self, *args, **kwargs):
        my_param = kwargs.pop('my_param', None)
        super().__init__(*args, **kwargs)
        if my_param is not None:
            vehicle = get_object_or_404(Travel, id=my_param)
            seats = Seat.objects.filter(vehicle=vehicle.id, is_available=True)
            self.fields["seat_numbers"].queryset = seats
        self.my_param = my_param

    class Meta:
        model = Ticket
        fields = ["seat_numbers"]
        
    def clean(self):
        cleaned_data = super().clean()
        num_passengers = len(cleaned_data.get("seat_numbers", []))
        self.cleaned_data["num_passengers"] = num_passengers
        if num_passengers < 1:
            raise forms.ValidationError("Please select at least one seat.")
        return cleaned_data

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return False
        if len(self.cleaned_data["seat_numbers"]) != self.cleaned_data["num_passengers"]:
            self.add_error("seat_numbers", "You must select one seat per passenger.")
            return False
        return True

    def save(self, commit=True):
        ticket = super().save(commit=False)
        if commit:
            ticket.num_passengers = self.cleaned_data["num_passengers"]
            ticket.save()
            ticket.book_seats(self.cleaned_data["seat_numbers"])
        return ticket

class SearchForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ["origin", "destination", "departure_time"]
        widgets = {
            "origin": forms.Select(attrs={"class": "form-control"}),
            "destination": forms.Select(attrs={"class": "form-control"}),
            "departure_time": forms.SelectDateWidget,
        }
