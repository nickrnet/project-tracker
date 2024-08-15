from django import forms

from .user.new_user_form import NewUserDataForm


class SignupForm(forms.ModelForm):
    current = NewUserDataForm()
