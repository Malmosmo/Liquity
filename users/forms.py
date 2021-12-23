from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
