from django import forms
from django.core.validators import MinValueValidator

from .models import Room, Booking
from django.core.exceptions import ValidationError
from datetime import date

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        date = forms.DateField(widget=forms.DateInput)
        fields = '__all__'
        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
            'date_to': forms.DateInput(attrs={'type': 'date'}),
        }
        exclude = {
            'tables_number'
        }


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        date = forms.DateField(validators=[MinValueValidator(date.today())],widget=forms.DateInput)
        time = forms.TimeField(widget=forms.TimeInput)
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),

        }
        exclude = {
            'user',
            'table',
            'timeTo'
        }


