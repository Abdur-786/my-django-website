from django.contrib import admin
from .models import Quiz, Question, QuizDetail

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')

@admin.register(QuizDetail)
class QuizDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'result', 'reward')
