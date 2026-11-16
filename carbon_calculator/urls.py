from django.urls import path
from . import views

app_name = 'carbon_calculator'

urlpatterns = [
    path('', views.carbon_calculator, name='carbon_calculator'),
]