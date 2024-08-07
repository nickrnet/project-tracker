from django.db import models

from core.models import core as core_models
from core.models import user as core_user_models
from . import issue_type as issue_type_models
from . import priority as priority_models
from . import status as status_models


class IssueActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class Issue(core_models.CoreModel):
    class Meta:
        ordering = ['-created_on']

    active_objects = IssueActiveManager()

    reporter = models.ForeignKey(core_user_models.User, on_delete=models.CASCADE, related_name='issuereporter_set')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='projectissues_set')
    built_in_type = models.ForeignKey(issue_type_models.BuiltInIssueType, on_delete=models.CASCADE, blank=True, null=True)
    custom_type = models.ForeignKey(issue_type_models.CustomIssueType, on_delete=models.CASCADE, blank=True, null=True)
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    built_in_status = models.OneToOneField(status_models.BuiltInIssueStatus, on_delete=models.CASCADE, blank=True, null=True)
    built_in_priority = models.OneToOneField(priority_models.BuiltInIssuePriority, on_delete=models.CASCADE, blank=True, null=True)
    assignee = models.ForeignKey(core_user_models.User, on_delete=models.CASCADE, related_name='issueassignee_set', blank=True, null=True)
    watchers = models.ManyToManyField(core_user_models.User, related_name='issuewatchers_set')

    # TODO: attachments, other things a bug/story/epic needs
