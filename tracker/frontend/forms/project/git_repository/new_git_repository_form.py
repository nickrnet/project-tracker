from django import forms


class NewGitRepositoryForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    url = forms.CharField(required=False)
    project_id = forms.CharField(required=False, widget=forms.HiddenInput())  # must be put in the form for the Project's New Git Repository POST to work
