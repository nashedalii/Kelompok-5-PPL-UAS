from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Booking, Court
from .forms import BookingForm, AdminBookingForm, TIME_SLOTS
from django.utils import timezone
from datetime import datetime, timedelta

def homepage(request):
    courts = Court.objects.all()
    return render(request, 'SewaSmash/homepage.html', {'courts': courts})

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('booking_confirmation', pk=booking.pk)
    else:
        form = BookingForm()
        
        # Handle AJAX request for time slot availability
        if 'check_availability' in request.GET:
            date = request.GET.get('date')
            court_id = request.GET.get('court')
            
            if date and court_id:
                # Get all time slots
                all_slots = TIME_SLOTS
                
                # Get booked slots
                booked_slots = set()
                bookings = Booking.objects.filter(
                    booking_date=date,
                    court_id=court_id,
                    status='APPROVED'
                )
                
                for booking in bookings:
                    start = datetime.combine(datetime.today(), booking.start_time)
                    for hour in range(booking.duration):
                        slot_time = (start + timedelta(hours=hour)).time()
                        booked_slots.add(slot_time.strftime('%H:%M'))
                
                # Separate available and booked slots
                available_slots = [(value, label) for value, label in all_slots if value not in booked_slots]
                booked_slots = [(value, label) for value, label in all_slots if value in booked_slots]
                
                return JsonResponse({
                    'available_slots': available_slots,
                    'booked_slots': booked_slots
                })
    
    return render(request, 'SewaSmash/booking_form.html', {'form': form})

def booking_confirmation(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'SewaSmash/booking_confirmation.html', {'booking': booking})

def schedule_view(request):
    bookings = Booking.objects.filter(
        status='APPROVED',
        booking_date__gte=timezone.now().date()
    ).order_by('booking_date', 'start_time')
    return render(request, 'SewaSmash/schedule.html', {'bookings': bookings})

# Admin views
@login_required
def admin_dashboard(request):
    pending_bookings = Booking.objects.filter(status='PENDING').count()
    today_bookings = Booking.objects.filter(booking_date=timezone.now().date()).count()
    total_courts = Court.objects.count()
    
    # Get recent bookings (last 5 bookings)
    recent_bookings = Booking.objects.all().order_by('-created_at')[:5]
    
    context = {
        'pending_bookings': pending_bookings,
        'today_bookings': today_bookings,
        'total_courts': total_courts,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'SewaSmash/dashboard.html', context)

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'SewaSmash/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Apply status filter
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        # Apply court filter
        court = self.request.GET.get('court')
        if court:
            queryset = queryset.filter(court_id=court)
            
        # Apply date filter
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(booking_date=date)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courts'] = Court.objects.all()
        return context

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'SewaSmash/booking_detail.html'
    context_object_name = 'booking'

class AdminBookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = AdminBookingForm
    template_name = 'SewaSmash/admin_booking_form.html'
    success_url = reverse_lazy('booking_list')

class AdminBookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = AdminBookingForm
    template_name = 'SewaSmash/admin_booking_form.html'
    success_url = reverse_lazy('booking_list')

class AdminBookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'SewaSmash/booking_delete.html'
    success_url = reverse_lazy('booking_list')

@login_required
def update_booking_status(request, pk):
    if request.method == 'POST' and request.is_ajax():
        booking = get_object_or_404(Booking, pk=pk)
        status = request.POST.get('status')
        if status in ['APPROVED', 'REJECTED']:
            booking.status = status
            booking.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
