from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import EnergySource, EnergyUsage


class EnergyFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='energyuser',
            password='StrongPassword123!',
        )
        self.other = get_user_model().objects.create_user(
            username='energyother',
            password='StrongPassword123!',
        )
        self.source = EnergySource.objects.create(
            sourceType='Test Solar',
            energyCost='0.15',
        )
        self.client.login(username='energyuser', password='StrongPassword123!')

    def test_user_only_sees_own_energy_usage(self):
        EnergyUsage.objects.create(
            user_ID=self.user,
            source_ID=self.source,
            date=date.today(),
            energyConsumed='5.50',
        )
        EnergyUsage.objects.create(
            user_ID=self.other,
            source_ID=self.source,
            date=date.today(),
            energyConsumed='99.00',
        )
        response = self.client.get(reverse('energy_app:energy_tracking'))
        self.assertContains(response, '5.50')
        self.assertNotContains(response, '99.00')

    def test_valid_and_invalid_energy_submission(self):
        response = self.client.post(reverse('energy_app:add_energy_usage'), {
            'date': date.today().isoformat(),
            'source_ID': self.source.pk,
            'energyConsumed': '12.50',
        })
        self.assertRedirects(response, reverse('energy_app:energy_tracking'))

        response = self.client.post(reverse('energy_app:add_energy_usage'), {
            'date': 'bad',
            'source_ID': '999999',
            'energyConsumed': 'oops',
        })
        self.assertEqual(response.status_code, 200)
