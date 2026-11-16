from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import date

from .models import Course


class CourseFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='courseuser',
            password='StrongPassword123!',
        )
        self.course = Course.objects.create(
            title='Test Course',
            date=date.today(),
            description='Description',
            content='Content',
        )

    def test_course_overview_and_detail(self):
        self.assertEqual(self.client.get(reverse('courses:course_overview')).status_code, 200)
        self.assertEqual(
            self.client.get(reverse('courses:course_detail', args=[self.course.pk])).status_code,
            200,
        )

    def test_enrollment_requires_login(self):
        response = self.client.post(reverse('courses:enroll_course', args=[self.course.pk]))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_enroll(self):
        self.client.login(username='courseuser', password='StrongPassword123!')
        response = self.client.post(reverse('courses:enroll_course', args=[self.course.pk]))
        self.assertRedirects(response, reverse('users:profile'))
        self.assertTrue(self.course.users_enrolled.filter(pk=self.user.pk).exists())
