from django import forms

from core.models import user as core_user_models


class UserDataForm(forms.Form):
    email = forms.EmailField()
    name_prefix = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    name_suffix = forms.CharField(required=False)
    secondary_email = forms.EmailField(required=False)
    home_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'tel'}))
    mobile_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'tel'}))
    work_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'type': 'tel'}))
    address_line_1 = forms.CharField(required=False)
    address_line_2 = forms.CharField(required=False)
    postal_code = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    country = forms.CharField(required=False)
    timezone = forms.CharField(required=False)
