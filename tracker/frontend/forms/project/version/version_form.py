from django import forms


class VersionDataForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    label = forms.CharField()
    release_date = forms.DateField(required=False, widget=forms.SelectDateWidget())  # TODO: The unset_date_selector template is hardcoded to match the project form... needs a refactor to be useful here for the verison template(s)
    is_active = forms.BooleanField(required=False)
