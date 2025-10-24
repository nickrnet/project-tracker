from django import forms


class NewVersionDataForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    label = forms.CharField()
    release_date = forms.DateField(required=False, widget=forms.SelectDateWidget())
    is_active = forms.BooleanField()
    project_id = forms.CharField(required=False, widget=forms.HiddenInput())  # must be put in the form for the Project's New Version POST to work
