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

    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    next = forms.CharField(required=False, widget=forms.HiddenInput())
