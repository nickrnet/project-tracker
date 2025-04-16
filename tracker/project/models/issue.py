from django.db import models

from core.models import core as core_models
from . import issue_type as issue_type_models
from . import priority as priority_models
from . import status as status_models
from . import component as component_models
from . import version as version_models
from . import severity as severity_models


class IssueData(core_models.CoreModel):

    # TODO: Make a create override function to validate the reporter and created_by are project members

    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")

    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    reporter = models.ForeignKey('core.CoreUser', on_delete=models.CASCADE, related_name='issuereporter_set')
    assignee = models.ForeignKey('core.CoreUser', on_delete=models.CASCADE, related_name='issueassignee_set', blank=True, null=True)
    watchers = models.ManyToManyField('core.CoreUser', related_name='issuewatcher_set')

    built_in_type = models.ForeignKey(issue_type_models.BuiltInIssueType, on_delete=models.CASCADE, blank=True, null=True)
    built_in_priority = models.ForeignKey(priority_models.BuiltInIssuePriority, on_delete=models.CASCADE, blank=True, null=True)
    built_in_status = models.ForeignKey(status_models.BuiltInIssueStatus, on_delete=models.CASCADE, blank=True, null=True)
    built_in_severity = models.ForeignKey(severity_models.BuiltInIssueSeverity, on_delete=models.CASCADE, blank=True, null=True)
    custom_type = models.ForeignKey(issue_type_models.CustomIssueType, on_delete=models.CASCADE, blank=True, null=True)
    custom_priority = models.ForeignKey(priority_models.CustomIssuePriority, on_delete=models.CASCADE, blank=True, null=True)
    custom_severity = models.ForeignKey(severity_models.CustomIssueSeverity, on_delete=models.CASCADE, blank=True, null=True)
    custom_status = models.ForeignKey(status_models.CustomIssueStatus, on_delete=models.CASCADE, blank=True, null=True)
    # TODO: Should these be ManyToManyFields?
    component = models.ForeignKey(component_models.Component, on_delete=models.CASCADE, blank=True, null=True)
    version = models.ForeignKey(version_models.Version, on_delete=models.CASCADE, blank=True, null=True)
    # TODO: attachments, other things a bug/story/epic/test needs


class IssueObjectManager(models.Manager):
    def get_next_sequence_number(self, project_id):
        try:
            return self.filter(current__project_id=project_id).latest('sequence').sequence + 1
        except self.model.DoesNotExist:
            return 1


class IssueActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)

    def list_built_in_types(self):
        """
        A helper method to get all built-in issue types, useful in views.

        Returns:
            list: All built-in issue types.
        """

        return issue_type_models.BuiltInIssueType.objects.all()

    def list_built_in_priorities(self):
        """
        A helper method to get all built-in issue priorities, useful in views.

        Returns:
            list: All built-in issue priorities.
        """

        return priority_models.BuiltInIssuePriority.objects.all()

    def list_built_in_statuses(self):
        """
        A helper method to get all built-in issue statuses, useful in views.

        Returns:
            list: All built-in issue statuses.
        """

        return status_models.BuiltInIssueStatus.objects.all()

    def list_built_in_severities(self):
        """
        A helper method to get all built-in issue severities, useful in views.

        Returns:
            list: All built-in issue severities.
        """

        return severity_models.BuiltInIssueSeverity.objects.all()

    def list_versions(self, project_id):
        """
        A helper method to get all versions for a project, useful in views.

        Args:
            project_id (project.Project): A project object.

        Returns:
            list: All versions for a project.
        """

        return version_models.Version.objects.filter(project_id=project_id)

    def list_components(self, project_id):
        """
        A helper method to get all components for a project, useful in views.

        Args:
            project_id (project.Project): A project object.

        Returns:
            list: All components for a project.
        """

        return component_models.Component.objects.filter(project_id=project_id)


class Issue(core_models.Sequenced):
    class Meta:
        ordering = ['-created_on']

    active_objects = IssueActiveManager()
    objects = IssueObjectManager()

    current = models.OneToOneField(IssueData, on_delete=models.CASCADE)

    # TODO: Make a create override function to validate the reporter and created_by are project members

    def list_built_in_types(self):
        """
        A helper method to get all built-in issue types, useful in views.

        Returns:
            list: All built-in issue types.
        """

        return issue_type_models.BuiltInIssueType.objects.all()

    def list_built_in_priorities(self):
        """
        A helper method to get all built-in issue priorities, useful in views.

        Returns:
            list: All built-in issue priorities.
        """

        return priority_models.BuiltInIssuePriority.objects.all()

    def list_built_in_statuses(self):
        """
        A helper method to get all built-in issue statuses, useful in views.

        Returns:
            list: All built-in issue statuses.
        """

        return status_models.BuiltInIssueStatus.objects.all()

    def list_built_in_severities(self):
        """
        A helper method to get all built-in issue severities, useful in views.

        Returns:
            list: All built-in issue severities.
        """

        return severity_models.BuiltInIssueSeverity.objects.all()

    def list_versions(self):
        """
        A helper method to get all versions for a project, useful in views.

        Returns:
            list: All versions for a project.
        """

        return version_models.Version.objects.filter(project_id=self.current.project.id)

    def list_components(self):
        """
        A helper method to get all components for a project, useful in views.

        Returns:
            list: All components for a project.
        """

        return component_models.Component.objects.filter(project_id=self.current.project.id)
