from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from services.models import ServiceType

from .models import Booking


class BookingFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='booker',
            password='StrongPassword123!',
        )
        self.service = ServiceType.objects.get(service_name='Consultation')
        self.client.login(username='booker', password='StrongPassword123!')

    def test_booking_page_and_valid_booking(self):
        response = self.client.get(reverse('bookings:main_bookings'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('bookings:create_booking', args=[self.service.pk]), {
            'date': (date.today() + timedelta(days=7)).isoformat(),
            'time': '12:00',
            'address': '123 Test Street',
            'reason': 'A valid reason',
        })
        self.assertRedirects(response, reverse('bookings:main_bookings'))
        self.assertTrue(Booking.objects.filter(user=self.user, service_type=self.service).exists())

    def test_invalid_booking_is_redisplayed(self):
        response = self.client.post(reverse('bookings:create_booking', args=[self.service.pk]), {
            'date': '2000-01-01',
            'time': '12:00',
            'address': '',
            'reason': 'Invalid',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please choose today or a future date.')

    def test_anonymous_user_is_redirected(self):
        self.client.logout()
        response = self.client.get(reverse('bookings:main_bookings'))
        self.assertEqual(response.status_code, 302)
