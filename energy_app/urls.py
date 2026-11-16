from django.urls import path
from . import views

app_name = 'energy_app'

urlpatterns = [
    path('energy_tracking/', views.energy_usage_tracking, name='energy_tracking'),
    path('add_energy_usage/', views.add_energy_usage_view, name='add_energy_usage'),
]