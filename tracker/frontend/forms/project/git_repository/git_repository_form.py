from django import forms


class GitRepositoryDataForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    url = forms.URLField(assume_scheme='https')
