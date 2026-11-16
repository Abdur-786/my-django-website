from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Note


class NoteFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='notesuser',
            password='StrongPassword123!',
        )
        self.other = get_user_model().objects.create_user(
            username='otheruser',
            password='StrongPassword123!',
        )
        self.client.login(username='notesuser', password='StrongPassword123!')

    def test_create_and_delete_own_note(self):
        response = self.client.post(reverse('notes:add_note'), {
            'title': 'Test note',
            'date': date.today().isoformat(),
            'note': 'Test content',
        })
        self.assertRedirects(response, reverse('notes:view_notes'))

        note = Note.objects.get(user=self.user, title='Test note')
        response = self.client.post(reverse('notes:delete_note', args=[note.pk]))
        self.assertRedirects(response, reverse('notes:view_notes'))
        self.assertFalse(Note.objects.filter(pk=note.pk).exists())

    def test_cannot_delete_another_users_note(self):
        note = Note.objects.create(
            user=self.other,
            title='Other note',
            date=date.today(),
            note='Private',
        )
        response = self.client.post(reverse('notes:delete_note', args=[note.pk]))
        self.assertRedirects(response, reverse('notes:view_notes'))
        self.assertTrue(Note.objects.filter(pk=note.pk).exists())

    def test_invalid_date_filter_is_safe(self):
        response = self.client.get(reverse('notes:view_notes'), {'date': 'not-a-date'})
        self.assertEqual(response.status_code, 200)
