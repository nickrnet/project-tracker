from django.db import models

from core.models import core as core_models
from core.models import user as core_user_models


class BuiltInIssueSeverityManager(models.Manager):
    def initialize_built_in_severities(self):
        """
        Keep this in sync with the BuiltInIssueSeverity.IssueSeverities class.
        """
        built_in_issue_severities = [
            ('e82b1549-0beb-44ee-926b-d03b5dd95aa7', 'MINOR', 'Minor'),
            ('9aaa5bfe-3150-4db1-ad02-ee47694f569b', 'MAJOR', 'Major'),
            ('8e0432d7-81c6-4a3d-a5c8-a2dfbba1b330', 'CRITICAL', 'Critical'),
            ]
        system_user = core_user_models.CoreUser.objects.get_or_create_system_user()

        for id, name, description in built_in_issue_severities:
            self.create(id=id, created_by=system_user, name=name, description=description)


class BuiltInIssueSeverity(core_models.CoreModel):
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'description']

    class IssueSeverities(models.TextChoices):
        MINOR = 'MINOR', 'Minor'
        MAJOR = 'MAJOR', 'Major'
        CRITICAL = 'CRITICAL', 'Critical'

    objects = BuiltInIssueSeverityManager()

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssueSeverityData(core_models.CoreModel):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssueSeverityActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class CustomIssueSeverity(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = CustomIssueSeverityActiveManager()

    current = models.ForeignKey(CustomIssueSeverityData, on_delete=models.CASCADE)
