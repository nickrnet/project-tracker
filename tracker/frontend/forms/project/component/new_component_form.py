from django import forms


class NewComponentDataForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    label = forms.CharField()
    is_active = forms.BooleanField()
    project_id = forms.CharField(required=False, widget=forms.HiddenInput())  # must be put in the form for the Project's New Component POST to work
