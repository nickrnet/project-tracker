from django import forms

from core.models import user as core_user_models


class NewUserDataForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = core_user_models.CoreUserData
        fields = [
            'first_name',
            'last_name',
            'email',
            'secondary_email',
            'home_phone',
            'mobile_phone',
            'work_phone',
            'address_line_1',
            'address_line_2',
            'postal_code',
            'city',
            'state',
            'timezone',
            'password',
        ]

    def save(self):
        core_user_models.CoreUser.objects.create_core_user_from_web(self.cleaned_data)


class NewUserForm(forms.ModelForm):
    core_user_data = NewUserDataForm()

    class Meta:
        model = core_user_models.CoreUser
        fields = [
            'core_user_data',
        ]
