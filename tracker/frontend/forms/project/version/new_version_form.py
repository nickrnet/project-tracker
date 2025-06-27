from django import forms


class NewVersionDataForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    label = forms.CharField()
    # release_date = forms.DateField(required=False, widget=forms.SelectDateWidget())  # TODO: The unset_date_selector template is hardcoded to match the project form... needs a refactor to be useful here for the verison template(s)
    is_active = forms.BooleanField()
    project_id = forms.CharField(required=False, widget=forms.HiddenInput())  # must be put in the form for the Project's New Component POST to work
