from django.db import models

from core.models import core as core_models
from . import issue_type as issue_type_models
from . import priority as priority_models
from . import status as status_models
from . import component as component_models
from . import version as version_models
from . import severity as severity_models
from . import project as project_models

from core.tasks.send_issue_update import send_issue_update_email


class IssueData(core_models.CoreModel):
    """
    Data about an issue.

    Parameters:
        issue (Issue): The issue this data is about.
        summary (str): The summary of the issue.
        description (str): A description of the issue.
        project (Project): The project the issue belongs to.
        reporter (CoreUser): The user who reported the issue.
        assignee (CoreUser): The user assigned to the issue.
        watchers (list of CoreUser): The users watching the issue.
        built_in_issue_type (BuiltInIssueType):
    """

    # TODO: Make a create override function to validate the reporter and created_by are project members

    issue = models.ForeignKey('Issue', on_delete=models.CASCADE, blank=True, null=True)

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
    component = models.ManyToManyField(to=component_models.Component, blank=True)
    version = models.ManyToManyField(to=version_models.Version, blank=True)
    # TODO: attachments, other things a bug/story/epic/test needs


class IssueObjectManager(models.Manager):
    def get_next_sequence_number(self, project_id):
        try:
            return self.filter(current__project_id=project_id).latest('sequence').sequence + 1
        except self.model.DoesNotExist:
            return 1

    def list_built_in_types(self):
        """
        A helper method to get all built-in issue types, useful in views.

        Returns:
            list: All built-in issue types.
        """

        return issue_type_models.BuiltInIssueType.objects.all().order_by('-created_on')

    def list_built_in_priorities(self):
        """
        A helper method to get all built-in issue priorities, useful in views.

        Returns:
            list: All built-in issue priorities.
        """

        return priority_models.BuiltInIssuePriority.objects.all().order_by('-created_on')

    def list_built_in_statuses(self):
        """
        A helper method to get all built-in issue statuses, useful in views.

        Returns:
            list: All built-in issue statuses.
        """

        return status_models.BuiltInIssueStatus.objects.all().order_by('-created_on')

    def list_built_in_severities(self):
        """
        A helper method to get all built-in issue severities, useful in views.

        Returns:
            list: All built-in issue severities.
        """

        return severity_models.BuiltInIssueSeverity.objects.all().order_by('-created_on')

    def list_versions(self, project_id):
        """
        A helper method to get all versions for a project, useful in views.

        Args:
            project_id (project.Project): A project object.

        Returns:
            list: All versions for a project.
        """

        return version_models.Version.objects.filter(project_id=project_id).order_by('-created_on')

    def list_components(self, project_id):
        """
        A helper method to get all components for a project, useful in views.

        Args:
            project_id (project.Project): A project object.

        Returns:
            list: All components for a project.
        """

        return component_models.Component.objects.filter(project_id=project_id).order_by('-created_on')


class IssueActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('current', 'project', 'current__built_in_type', 'current__built_in_priority', 'current__built_in_status', 'current__built_in_severity', 'current__reporter', 'current__assignee').filter(deleted=None).order_by('-created_on')

    def list_built_in_types(self):
        """
        A helper method to get all built-in issue types, useful in views.

        Returns:
            list: All built-in issue types.
        """

        return issue_type_models.BuiltInIssueType.active_objects.all().order_by('-created_on')

    def list_built_in_priorities(self):
        """
        A helper method to get all built-in issue priorities, useful in views.

        Returns:
            list: All built-in issue priorities.
        """

        return priority_models.BuiltInIssuePriority.active_objects.all().order_by('-created_on')

    def list_built_in_statuses(self):
        """
        A helper method to get all built-in issue statuses, useful in views.

        Returns:
            list: All built-in issue statuses.
        """

        return status_models.BuiltInIssueStatus.active_objects.all().order_by('-created_on')

    def list_built_in_severities(self):
        """
        A helper method to get all built-in issue severities, useful in views.

        Returns:
            list: All built-in issue severities.
        """

        return severity_models.BuiltInIssueSeverity.active_objects.all().order_by('-created_on')

    def list_versions(self, project_id):
        """
        A helper method to get all versions for a project, useful in views.

        Args:
            project_id (project.Project): A project object.

        Returns:
            list: All versions for a project.
        """

        return version_models.Version.active_objects.filter(project_id=project_id).order_by('-created_on')

    def list_components(self, project_id):
        """
        A helper method to get all components for a project, useful in views.

        Args:
            project_id (project.Project): A project object.

        Returns:
            list: All components for a project.
        """

        return component_models.Component.active_objects.filter(project_id=project_id).order_by('-created_on')


class Issue(core_models.Sequenced):
    """
    An issue.

    Parameters:
        current (IssueData): The current data for this issue.
        project (Project): The project this issue is associated with.
    """

    class Meta:
        ordering = ['-created_on']

    active_objects = IssueActiveManager()
    objects = IssueObjectManager()

    current = models.OneToOneField(IssueData, on_delete=models.CASCADE, related_name='current')
    project = models.ForeignKey(project_models.Project, on_delete=models.CASCADE)

    # TODO: Links to other issues
    # TODO: Make a create override function to validate the reporter and created_by are project members, currently handled by views

    def send_issue_update_email(self, issue_url):
        """
        Sends an issue update email.

        Args:
            issue_url (str): The URL for the issue.
        """

        # TODO: Add watchers, etc.
        to_email = self.current.reporter.current.email

        send_issue_update_email.delay(
            to_email,
            self.current.project.label.current.label + "-" + str(self.sequence),
            issue_url,
            )
