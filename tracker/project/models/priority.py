from django.db import models

from core.models import core as core_models
from core.models import user as core_user_models


class BuiltInIssuePriorityManager(models.Manager):
    def initialize_built_in_priorities(self):
        """
        Keep this in sync with the BuiltInIssuePriorities.IssuePriorities class.
        """
        built_in_issue_priorities = [
            ('cbb014f3-f9ab-46da-926e-7d76bca69470', 'CRITICAL', 'Critical'),
            ('376295d8-2132-410f-a9aa-4e32757f5324', 'HIGH', 'High'),
            ('9756bb3a-521f-40a1-ae26-d1d2ecf2a54d', 'MEDIUM', 'Medium'),
            ('91dcbc0e-8189-4505-83e2-70892bb3bc26', 'LOW', 'Low'),
            ]
        system_user = core_user_models.CoreUser.objects.get_or_create_system_user()

        for id, name, description in built_in_issue_priorities:
            self.create(id=id, created_by=system_user, name=name, description=description)


class BuiltInIssuePriority(core_models.CoreModel):
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'description']

    class IssuePriorities(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    objects = BuiltInIssuePriorityManager()

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssuePriorityData(core_models.CoreModel):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssuePriorityActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class CustomIssuePriority(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = CustomIssuePriorityActiveManager()

    current = models.ForeignKey(CustomIssuePriorityData, on_delete=models.CASCADE)
