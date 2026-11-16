from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'date', 'note']
        widgets = {
            'date': forms.SelectDateWidget(years=range(2000,2030)),
        }