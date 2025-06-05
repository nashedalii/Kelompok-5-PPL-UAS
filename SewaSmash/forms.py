from django import forms
from .models import Booking, Court
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta, time

TIME_SLOTS = [
    ('06:00', '06:00'), ('07:00', '07:00'), ('08:00', '08:00'),
    ('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'),
    ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'),
    ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'),
    ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00'),
    ('21:00', '21:00'), ('22:00', '22:00'), ('23:00', '23:00'),
]

class BookingForm(forms.ModelForm):
    start_time = forms.ChoiceField(
        choices=TIME_SLOTS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['customer_name', 'court', 'booking_date', 'start_time', 'duration', 'phone_number']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'court': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '4'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.data.get('booking_date') and self.data.get('court'):
            # Get booked time slots for the selected date and court
            booked_slots = self.get_booked_slots()
            # Update time slot choices
            available_choices = [(value, label) for value, label in TIME_SLOTS if value not in booked_slots]
            self.fields['start_time'].choices = available_choices

    def get_booked_slots(self):
        """Get all booked time slots for the selected date and court"""
        booking_date = self.data.get('booking_date')
        court_id = self.data.get('court')
        
        if not booking_date or not court_id:
            return set()

        # Get all approved bookings for the selected date and court
        bookings = Booking.objects.filter(
            booking_date=booking_date,
            court_id=court_id,
            status='APPROVED'
        ).exclude(pk=self.instance.pk if self.instance else None)

        booked_slots = set()
        for booking in bookings:
            start = datetime.strptime(str(booking.start_time), '%H:%M:%S')
            # Block all slots within the booking duration
            for hour in range(booking.duration):
                slot_time = (start + timedelta(hours=hour)).strftime('%H:%M')
                booked_slots.add(slot_time)

        return booked_slots

    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        start_time = cleaned_data.get('start_time')
        duration = cleaned_data.get('duration')
        court = cleaned_data.get('court')

        if booking_date and start_time and duration and court:
            # Check if booking date is not in the past
            if booking_date < timezone.now().date():
                raise ValidationError("Booking date cannot be in the past")

            # Convert start_time string to time object
            start_time = datetime.strptime(start_time, '%H:%M').time()

            # Check for overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                court=court,
                booking_date=booking_date,
                status='APPROVED'
            ).exclude(pk=self.instance.pk if self.instance else None)

            for booking in overlapping_bookings:
                booking_end_time = (
                    datetime.combine(booking_date, booking.start_time) +
                    timedelta(hours=booking.duration)
                ).time()
                new_booking_end_time = (
                    datetime.combine(booking_date, start_time) +
                    timedelta(hours=duration)
                ).time()

                if (start_time < booking_end_time and 
                    new_booking_end_time > booking.start_time):
                    raise ValidationError(
                        "This time slot overlaps with an existing booking"
                    )

        return cleaned_data

class AdminBookingForm(BookingForm):
    class Meta(BookingForm.Meta):
        fields = BookingForm.Meta.fields + ['status']
        widgets = {
            **BookingForm.Meta.widgets,
            'status': forms.Select(attrs={'class': 'form-control'})
        } 