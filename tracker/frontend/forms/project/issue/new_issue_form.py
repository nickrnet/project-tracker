from django import forms

from project.models import component as component_models
from project.models import version as version_models


class NewIssueForm(forms.Form):
    summary = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea)
    project = forms.UUIDField()
    reporter = forms.UUIDField()
    assignee = forms.UUIDField(required=False)
    watchers = forms.UUIDField(required=False)
    built_in_type = forms.UUIDField(required=False)
    built_in_priority = forms.UUIDField(required=False)
    built_in_status = forms.UUIDField(required=False)
    built_in_severity = forms.UUIDField(required=False)
    version = forms.ModelMultipleChoiceField(required=False, queryset=version_models.Version.objects.all())
    component = forms.ModelMultipleChoiceField(required=False, queryset=component_models.Component.objects.all())
