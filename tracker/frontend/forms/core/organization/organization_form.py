from django import forms
from django.utils import timezone

from core.models import user as core_user_models
from core.models import organization as core_organization_models


class OrganizationDataForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, required=False)
    responsible_party_email = forms.CharField(max_length=255)
    responsible_party_phone = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'type': 'tel'}))
    address_line_1 = forms.CharField(max_length=255)
    address_line_2 = forms.CharField(max_length=255, required=False)
    postal_code = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    state = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    timezone = forms.CharField(max_length=255, required=False, initial=timezone.get_default_timezone_name())

    is_paid = forms.BooleanField(required=False)
    renewal_date = forms.DateField(required=False, widget=forms.SelectDateWidget())
    number_users_allowed = forms.IntegerField(required=False)


class OrganizationForm(forms.ModelForm):
    current = OrganizationDataForm()

    class Meta:
        model = core_organization_models.Organization
        fields = [
            'current',
            ]
