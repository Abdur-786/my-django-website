from django.test import TestCase
from django.urls import reverse


class CarbonCalculatorTests(TestCase):
    def test_valid_calculation(self):
        response = self.client.post(reverse('carbon_calculator:carbon_calculator'), {
            'diet': 'omnivore',
            'transport': 'car',
            'people': '2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '4.0 units')

    def test_bad_input_is_handled(self):
        response = self.client.post(reverse('carbon_calculator:carbon_calculator'), {
            'diet': 'not-valid',
            'transport': 'not-valid',
            'people': '0',
        })
        self.assertEqual(response.status_code, 200)
