from django import forms

from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'next',
        ]

    next = forms.CharField(required=False, widget=forms.HiddenInput())
    password = forms.CharField(required=False, widget=forms.PasswordInput())
