from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_overview, name='course_overview'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
]
