import uuid

from django.db import models

from core.models import core as core_models
from core.models import user as core_user_models


class BuiltInIssueSeverityData(core_models.CoreModel):
    """
    Data about a built-in issue severity.

    Parameters:
        built_in_issue_severity (BuiltInIssueSeverity): The built-in issue severity.
        name (str): The name of the built-in issue severity.
        description (str): A description of the built-in issue severity.
    """

    built_in_issue_severity = models.ForeignKey('BuiltInIssueSeverity', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class BuiltInIssueSeverityManager(models.Manager):
    def initialize_built_in_issue_severities(self) -> None:
        """
        Initializes built-in issue severities.
        """

        # We force specific UUIDs here to ensure consistency across all installations.
        built_in_issue_severities = [
            ('8e0432d7-81c6-4a3d-a5c8-a2dfbba1b330', 'CRITICAL', 'Critical'),
            ('9aaa5bfe-3150-4db1-ad02-ee47694f569b', 'MAJOR', 'Major'),
            ('e82b1549-0beb-44ee-926b-d03b5dd95aa7', 'MINOR', 'Minor'),
            ]
        system_user = core_user_models.CoreUser.objects.get_or_create_system_user()

        existing_built_in_issue_severities = self.all().values_list('id', flat=True)
        for id, name, description in built_in_issue_severities:
            if uuid.UUID(id) not in existing_built_in_issue_severities:
                built_in_issue_severity_data = BuiltInIssueSeverityData.objects.create(created_by=system_user, name=name, description=description)
                built_in_issue_severity = self.create(id=id, created_by=system_user, current=built_in_issue_severity_data)
                built_in_issue_severity_data.built_in_issue_severity = built_in_issue_severity
                built_in_issue_severity_data.save()
            else:
                built_in_issue_severity = self.get(id=id)
                built_in_issue_severity_data = BuiltInIssueSeverityData.objects.create(created_by=system_user, built_in_issue_severity=built_in_issue_severity, name=name, description=description)
                built_in_issue_severity.current = built_in_issue_severity_data
                built_in_issue_severity.save()


class BuiltInIssueSeverity(core_models.CoreModel):
    """
    Built-in issue severity.

    Parameters:
        current (BuiltInIssueSeverityData): The current data for this built-in issue severity.
    """

    class Meta:
        ordering = ['current__name']

    objects = BuiltInIssueSeverityManager()

    current = models.OneToOneField(BuiltInIssueSeverityData, on_delete=models.CASCADE)


class CustomIssueSeverityData(core_models.CoreModel):
    """
    Data about a custom issue severity.

    Parameters:
        custom_issue_severity (CustomIssueSeverity): The custom issue severity this data is about.
        name (str): The name of the custom issue severity.
        description (str): A description of the custom issue severity.
    """

    class Meta:
        ordering = ['name']

    custom_issue_severity = models.ForeignKey('CustomIssueSeverity', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssueSeverityActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('current').filter(deleted=None)


class CustomIssueSeverity(core_models.CoreModel):
    """
    Custom issue severity model.

    Parameters:
        current (CustomIssueSeverityData): Data about the custom issue severity.
    """

    class Meta:
        ordering = ['current__name']

    active_objects = CustomIssueSeverityActiveManager()

    current = models.OneToOneField(CustomIssueSeverityData, on_delete=models.CASCADE)
