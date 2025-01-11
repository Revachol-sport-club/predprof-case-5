from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()


class ExtendedUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-standart-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-standart-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-standart-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-standart-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-standart-input'}),
        }