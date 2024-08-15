from django import forms


class GitRepositoryDataForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    url = forms.CharField(required=False)
