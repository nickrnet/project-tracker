from django.db import models

from core.models import core as core_models
from core.models import user as core_user_models


class BuiltInIssueStatusManager(models.Manager):
    def initialize_built_in_statuses(self):
        """
        Keep this in sync with the BuiltInIssueStatuses.IssueStatuses class.
        """
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

        for id, name, description in built_in_issue_statuses:
            self.create(id=id, created_by=system_user, name=name, description=description)


class BuiltInIssueStatus(core_models.CoreModel):
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'description']

    class IssueStatuses(models.TextChoices):
        TRIAGE = 'TRIAGE', 'Triage'
        OPEN = 'OPEN', 'Open'
        READY_FOR_DEVELOPMENT = 'READY_FOR_DEVELOPMENT', 'Ready for Development'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
        COMPLETE = 'COMPLETE', 'Complete'
        CLOSED = 'CLOSED', 'Closed'

    objects = BuiltInIssueStatusManager()

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssueStatusData(core_models.CoreModel):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssueStatusActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class CustomIssueStatus(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = CustomIssueStatusActiveManager()

    current = models.ForeignKey(CustomIssueStatusData, on_delete=models.CASCADE)
