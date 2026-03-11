from django import forms


class ComponentDataForm(forms.Form):
    name = forms.CharField()
    description = forms.CharField(required=False)
    label = forms.CharField()
    is_active = forms.BooleanField()
