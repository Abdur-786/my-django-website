from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserFlowTests(TestCase):
    def test_register_login_profile_logout(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'password1': 'StrongPassword123!',
            'password2': 'StrongPassword123!',
        })
        self.assertRedirects(response, reverse('users:profile'))

        user = get_user_model().objects.get(username='newuser')
        self.assertTrue(user.is_authenticated)

        self.client.get(reverse('users:logout'))
        response = self.client.post(reverse('users:login'), {
            'username': 'newuser',
            'password': 'StrongPassword123!',
        })
        self.assertRedirects(response, reverse('users:profile'))

    def test_invalid_login_is_handled(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'missing',
            'password': 'wrong',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')
