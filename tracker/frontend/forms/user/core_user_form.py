from django import forms

from core.models import user as core_user_models


class CoreUserDataForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = core_user_models.CoreUserData
        fields = [
            'email',
            'name_prefix',
            'first_name',
            'middle_name',
            'last_name',
            'name_suffix',
            'secondary_email',
            'home_phone',
            'mobile_phone',
            'work_phone',
            'address_line_1',
            'address_line_2',
            'postal_code',
            'city',
            'state',
            'country',
            'timezone',
        ]

    def save(self):
        self.cleaned_data.pop('password')
        core_user_models.CoreUserData.objects.update(**self.cleaned_data)


class CoreUserForm(forms.ModelForm):
    core_user_data = CoreUserDataForm()

    class Meta:
        model = core_user_models.CoreUser
        fields = [
            'core_user_data',
        ]
