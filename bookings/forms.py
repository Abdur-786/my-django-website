from django import forms
from django.utils import timezone

from .models import Booking
from services.models import ServiceType


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'address', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'address': forms.TextInput(attrs={'autocomplete': 'street-address'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_date(self):
        booking_date = self.cleaned_data['date']
        if booking_date < timezone.localdate():
            raise forms.ValidationError('Please choose today or a future date.')
        return booking_date

    def clean_time(self):
        booking_time = self.cleaned_data['time']
        booking_date = self.cleaned_data.get('date')
        if booking_date == timezone.localdate() and booking_time < timezone.localtime().time():
            raise forms.ValidationError('Please choose a future time.')
        return booking_time


class ServiceSelectionForm(forms.Form):
    service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all().order_by('service_name'),
        empty_label='Choose a service',
    )
