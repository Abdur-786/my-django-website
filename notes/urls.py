from django.urls import path
from .import views

app_name = 'notes'

urlpatterns = [
    path('add/',views.add_note,name='add_note'),
    path('views/',views.view_notes,name='view_notes'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
]