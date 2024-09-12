from django import forms

from .core.user.new_user_form import NewUserForm


class SignupForm(forms.ModelForm):
    current = NewUserForm()
