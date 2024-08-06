from django import forms

from core.models import user as core_user_models


class CoreUserDataForm(forms.Form):
    email = forms.EmailField()
    name_prefix = forms.CharField(required=False)
    first_name = forms.CharField()
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField()
    name_suffix = forms.CharField(required=False)
    secondary_email = forms.EmailField(required=False)
    home_phone = forms.CharField(required=False)
    mobile_phone = forms.CharField(required=False)
    work_phone = forms.CharField(required=False)
    address_line_1 = forms.CharField()
    address_line_2 = forms.CharField(required=False)
    postal_code = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    country = forms.CharField()
    timezone = forms.CharField()

    def save(self):
        core_user_models.CoreUserData.objects.update(**self.cleaned_data)


class CoreUserForm(forms.ModelForm):
    core_user_data = CoreUserDataForm()

    class Meta:
        model = core_user_models.CoreUser
        fields = [
            'core_user_data',
        ]
