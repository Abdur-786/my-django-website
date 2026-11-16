from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, ServiceSelectionForm
from .models import Booking
from services.models import ServiceType


@login_required
def main_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('service_type').order_by('date', 'time')
    service_form = ServiceSelectionForm(request.POST or None)

    if request.method == 'POST' and service_form.is_valid():
        service = service_form.cleaned_data['service_type']
        return redirect('bookings:create_booking', service_id=service.pk)

    return render(request, 'bookings/main_bookings.html', {
        'bookings': bookings,
        'service_form': service_form,
    })


@login_required
def create_booking(request, service_id):
    service = get_object_or_404(ServiceType, pk=service_id)
    form = BookingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.service_type = service
        booking.save()
        messages.success(request, f'{service.service_name} booking created successfully.')
        return redirect('bookings:main_bookings')

    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'service': service,
    })


@login_required
def consultation_booking(request):
    service = ServiceType.objects.filter(service_name__iexact='Consultation').first()
    if service is None:
        messages.error(request, 'The consultation service is currently unavailable.')
        return redirect('bookings:main_bookings')
    return create_booking(request, service.pk)


@login_required
def installation_booking(request):
    service = ServiceType.objects.filter(service_name__iexact='Installation').first()
    if service is None:
        messages.error(request, 'The installation service is currently unavailable.')
        return redirect('bookings:main_bookings')
    return create_booking(request, service.pk)
