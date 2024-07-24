from django import forms

from .user.new_user_form import NewUserDataForm


class SignupForm(forms.ModelForm):
    core_user_data = NewUserDataForm()
