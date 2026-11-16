from django.urls import path

from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('my/', views.quizzes, name='quizzes'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/form/', views.quiz_form, name='quiz_form'),
    path('<int:quiz_id>/result/', views.result, name='result'),
]
