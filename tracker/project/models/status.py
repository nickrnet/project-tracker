import uuid

from django.db import models

from core.models import core as core_models
from core.models import user as core_user_models


class BuiltInIssueStatusData(core_models.CoreModel):
    """
    Data about a built-in issue status.

    Parameters:
        built_in_issue_status (BuiltInIssueStatus): The built-in issue status this data is about.
        name (str): The name of the built-in issue status.
        description (str): The description of the built-in issue status.
    """

    built_in_issue_status = models.ForeignKey('BuiltInIssueStatus', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class BuiltInIssueStatusManager(models.Manager):
    def initialize_built_in_issue_statuses(self):
        """
        Initializes built-in issue statuses.
        """

        # We force specific UUIDs here to ensure consistency across all installations.
        built_in_issue_statuses = [
            ('24c03dc0-a98f-4125-a9db-51781e610444', 'CLOSED', 'Closed'),
            ('24494695-c0f8-4a90-aacc-670776b40ff9', 'COMPLETE', 'Complete'),
            ('bef3f9f1-0f37-41be-b405-322731c76b16', 'RESOLVED', 'Resolved'),
            ('332f5852-a6e1-415f-bef5-44fcd36dbfc9', 'IN_PROGRESS', 'In Progress'),
            ('4c509937-972d-470c-9589-362ba90c1268', 'READY_FOR_DEVELOPMENT', 'Ready for Development'),
            ('86780f1e-e3a8-4869-bc6b-1e9a3111ef9f', 'OPEN', 'Open'),
            ('34d28f8e-dd1c-4871-938b-3ed56f960093', 'TRIAGE', 'Triage'),
            ]
        system_user = core_user_models.CoreUser.objects.get_or_create_system_user()

        existing_built_in_issue_statuses = self.all().values_list('id', flat=True)
        for id, name, description in built_in_issue_statuses:
            if uuid.UUID(id) not in existing_built_in_issue_statuses:
                built_in_status_data = BuiltInIssueStatusData.objects.create(created_by=system_user, name=name, description=description)
                built_in_status = self.create(id=id, created_by=system_user, current=built_in_status_data)
                built_in_status_data.built_in_issue_status = built_in_status
                built_in_status_data.save()
            else:
                built_in_status = self.get(id=id)
                built_in_status_data = BuiltInIssueStatusData.objects.create(created_by=system_user, built_in_issue_status=built_in_status, name=name, description=description)
                built_in_status.current = built_in_status_data
                built_in_status.save()


class BuiltInIssueStatus(core_models.CoreModel):
    """
    A built-in issue status.

    Parameters:
        current (BuiltInIssueStatus): The data about the built-in issue status.
    """

    class Meta:
        ordering = ['current__name']

    objects = BuiltInIssueStatusManager()

    current = models.OneToOneField(BuiltInIssueStatusData, on_delete=models.CASCADE)


class CustomIssueStatusData(core_models.CoreModel):
    """
    Data about a custom issue status.

    Parameters:
        custom_issue_status (CustomIssueStatus): The status this data is about.
        name (str): The name of the custom status.
        description (str): The description of the custom status.
    """

    class Meta:
        ordering = ['name']

    custom_issue_status = models.ForeignKey('CustomIssueStatus', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssueStatusActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('current').filter(deleted=None)


class CustomIssueStatus(core_models.CoreModel):
    """
    Custom issue status.

    Parameters:
        current (CustomIssueStatusData): The data of the custom issue status.
    """

    class Meta:
        ordering = ['current__name']

    active_objects = CustomIssueStatusActiveManager()

    current = models.OneToOneField(CustomIssueStatusData, on_delete=models.CASCADE)
