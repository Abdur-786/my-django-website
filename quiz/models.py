from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    answ1 = models.CharField(max_length=255)
    answ2 = models.CharField(max_length=255)
    answ3 = models.CharField(max_length=255)
    correct = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        choices=[(1, 'Answer 1'), (2, 'Answer 2'), (3, 'Answer 3')],
    )

    def __str__(self):
        return self.text


class QuizDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    result = models.FloatField()
    reward = models.CharField(
        max_length=10,
        choices=[
            ('gold', 'Gold'),
            ('silver', 'Silver'),
            ('bronze', 'Bronze'),
            ('no reward', 'No Reward'),
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'quiz'], name='unique_user_quiz_result'),
        ]

    def __str__(self):
        return f'{self.user} - {self.quiz}'
