from django import forms


class NewIssueForm(forms.Form):
    project = forms.UUIDField()
    reporter = forms.UUIDField()
    summary = forms.CharField()
    description = forms.CharField(required=False)
    assignee = forms.UUIDField(required=False)
    watchers = forms.UUIDField(required=False)
    built_in_type = forms.UUIDField(required=False)
    built_in_priority = forms.UUIDField(required=False)
    built_in_status = forms.UUIDField(required=False)
