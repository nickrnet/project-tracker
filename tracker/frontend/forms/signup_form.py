from django import forms

from .core.user.new_user_form import NewUserDataForm


class SignupForm(forms.ModelForm):
    current = NewUserDataForm()
