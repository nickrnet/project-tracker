from django import forms


class ProjectDataForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    label = forms.CharField(required=False)
    is_active = forms.BooleanField(required=False)
    is_private = forms.BooleanField(required=False)
    start_date = forms.DateField(required=False, widget=forms.SelectDateWidget())
    end_date = forms.DateField(required=False, widget=forms.SelectDateWidget())
    git_repository = forms.UUIDField(required=False)
