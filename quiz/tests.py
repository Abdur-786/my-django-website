from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Question, Quiz, QuizDetail


class QuizFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='quizuser',
            password='StrongPassword123!',
        )
        self.quiz = Quiz.objects.create(name='Test Quiz')
        self.questions = [
            Question.objects.create(
                quiz=self.quiz,
                text='Question 1',
                answ1='Correct',
                answ2='Wrong',
                answ3='Wrong',
                correct=1,
            ),
            Question.objects.create(
                quiz=self.quiz,
                text='Question 2',
                answ1='Wrong',
                answ2='Correct',
                answ3='Wrong',
                correct=2,
            ),
        ]
        self.client.login(username='quizuser', password='StrongPassword123!')

    def test_quiz_requires_all_answers(self):
        response = self.client.post(reverse('quiz:quiz_form', args=[self.quiz.pk]), {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(QuizDetail.objects.filter(user=self.user, quiz=self.quiz).exists())

    def test_valid_quiz_creates_result(self):
        response = self.client.post(reverse('quiz:quiz_form', args=[self.quiz.pk]), {
            f'question-{self.questions[0].pk}': '1',
            f'question-{self.questions[1].pk}': '2',
        })
        self.assertRedirects(response, reverse('quiz:result', args=[self.quiz.pk]))
        detail = QuizDetail.objects.get(user=self.user, quiz=self.quiz)
        self.assertEqual(detail.result, 100)
        self.assertEqual(detail.reward, 'gold')

    def test_non_integer_answer_is_safe(self):
        response = self.client.post(reverse('quiz:quiz_form', args=[self.quiz.pk]), {
            f'question-{question.pk}': 'abc'
            for question in self.questions
        })
        self.assertEqual(response.status_code, 200)

    def test_empty_quiz_does_not_divide_by_zero(self):
        empty_quiz = Quiz.objects.create(name='Empty Quiz')
        response = self.client.post(reverse('quiz:quiz_form', args=[empty_quiz.pk]), {})
        self.assertRedirects(response, reverse('quiz:quiz_detail', args=[empty_quiz.pk]))
