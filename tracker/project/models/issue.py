from django.db import models

from core.models import core as core_models
from . import issue_type as issue_type_models
from . import priority as priority_models
from . import status as status_models
from . import component as component_models
from . import version as version_models
from . import severity as severity_models


class IssueData(core_models.CoreModel):
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


class IssueActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class Issue(core_models.CoreModel):
    class Meta:
        ordering = ['-created_on']

    active_objects = IssueActiveManager()

    current = models.OneToOneField(IssueData, on_delete=models.CASCADE)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    reporter = models.ForeignKey('core.CoreUser', on_delete=models.CASCADE, related_name='issuereporter_set')
    assignee = models.ForeignKey('core.CoreUser', on_delete=models.CASCADE, related_name='issueassignee_set', blank=True, null=True)
    watchers = models.ManyToManyField('core.CoreUser', related_name='issuewatcher_set')
    built_in_type = models.ForeignKey(issue_type_models.BuiltInIssueType, on_delete=models.CASCADE, blank=True, null=True)
    custom_type = models.ForeignKey(issue_type_models.CustomIssueType, on_delete=models.CASCADE, blank=True, null=True)
    built_in_priority = models.OneToOneField(priority_models.BuiltInIssuePriority, on_delete=models.CASCADE, blank=True, null=True)
    custom_priority = models.OneToOneField(priority_models.CustomIssuePriority, on_delete=models.CASCADE, blank=True, null=True)
    built_in_status = models.OneToOneField(status_models.BuiltInIssueStatus, on_delete=models.CASCADE, blank=True, null=True)
    custom_status = models.OneToOneField(status_models.CustomIssueStatus, on_delete=models.CASCADE, blank=True, null=True)
    built_in_severity = models.ForeignKey(severity_models.BuiltInIssueSeverity, on_delete=models.CASCADE, blank=True, null=True)
    custom_severity = models.ForeignKey(severity_models.CustomIssueSeverity, on_delete=models.CASCADE, blank=True, null=True)
    version = models.ForeignKey(version_models.Version, on_delete=models.CASCADE, blank=True, null=True)
    component = models.ForeignKey(component_models.Component, on_delete=models.CASCADE, blank=True, null=True)
    # TODO: attachments, other things a bug/story/epic needs
