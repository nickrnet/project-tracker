from django import forms


class IssueForm(forms.Form):
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
    version = forms.UUIDField(required=False)
    component = forms.UUIDField(required=False)
