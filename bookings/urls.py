from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.main_bookings, name='main_bookings'),
    path('create/<int:service_id>/', views.create_booking, name='create_booking'),
    path('consultation/', views.consultation_booking, name='consultation_booking'),
    path('installation/', views.installation_booking, name='installation_booking'),
]
