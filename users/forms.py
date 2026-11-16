from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import MyUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'image', 'about', 'dateOfBirth']
        widgets = {
            'dateOfBirth': forms.DateInput(attrs={'type': 'date'}),
            'about': forms.Textarea(attrs={'rows': 5}),
        }
