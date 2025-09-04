from django import forms


class VersionDataForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    label = forms.CharField()
    release_date = forms.DateField(required=False, widget=forms.SelectDateWidget())
    is_active = forms.BooleanField(required=False)
