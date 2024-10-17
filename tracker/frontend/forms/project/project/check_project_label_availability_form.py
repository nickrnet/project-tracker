from django import forms


class ProjectLabelAvailabilityForm(forms.Form):
    label = forms.CharField()
