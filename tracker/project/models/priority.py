import uuid

from django.db import models

from core.models import core as core_models
from core.models import user as core_user_models


class BuiltInIssuePriorityData(core_models.CoreModel):
    """
    Data about a built-in issue priority.

    Parameters:
        built_in_issue_priority (BuiltInIssuePriority): The built-in issue priority.
        name (str): The name of the BuiltInIssuePriority.
        description (str): A description of the BuiltInIssuePriority.
    """

    built_in_issue_priority = models.ForeignKey('BuiltInIssuePriority', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default='')


class BuiltInIssuePriorityManager(models.Manager):
    def initialize_built_in_issue_priorities(self):
        """
        Initializes BuiltInIssuePriorities.
        """

        # We force specific UUIDs here to ensure consistency across all installations.
        built_in_issue_priorities = [
            ('cbb014f3-f9ab-46da-926e-7d76bca69470', 'CRITICAL', 'Critical'),
            ('376295d8-2132-410f-a9aa-4e32757f5324', 'HIGH', 'High'),
            ('9756bb3a-521f-40a1-ae26-d1d2ecf2a54d', 'MEDIUM', 'Medium'),
            ('91dcbc0e-8189-4505-83e2-70892bb3bc26', 'LOW', 'Low'),
            ]
        system_user = core_user_models.CoreUser.objects.get_or_create_system_user()

        existing_built_in_issue_priorities = self.all().values_list('id', flat=True)
        for id, name, description in built_in_issue_priorities:
            if uuid.UUID(id) not in existing_built_in_issue_priorities:
                built_in_issue_priority_data = BuiltInIssuePriorityData.objects.create(created_by=system_user, name=name, description=description)
                built_in_issue_priority = self.create(id=id, created_by=system_user, current=built_in_issue_priority_data)
                built_in_issue_priority_data.built_in_issue_priority = built_in_issue_priority
                built_in_issue_priority_data.save()
            else:
                built_in_issue_priority = self.get(id=id)
                built_in_issue_priority_data = BuiltInIssuePriorityData.objects.create(created_by=system_user, built_in_issue_priority=built_in_issue_priority, name=name, description=description)
                built_in_issue_priority.current = built_in_issue_priority_data
                built_in_issue_priority.save()


class BuiltInIssuePriority(core_models.CoreModel):
    """
    Built-in issue priority.

    Parameters:
        current (BuiltInIssuePriorityData): The data about the built-in issue priority.
    """

    class Meta:
        ordering = ['current__name']

    objects = BuiltInIssuePriorityManager()

    current = models.OneToOneField(BuiltInIssuePriorityData, on_delete=models.CASCADE)


class CustomIssuePriorityData(core_models.CoreModel):
    """
    Custom issue priority data.

    Parameters:
       custom_issue_priority (CustomIssuePriority): The custom issue priority this data is about.
       name (str): The name of the custom issue priority.
       description (str): The description of the custom issue priority.
    """

    class Meta:
        ordering = ['name']

    custom_issue_priority = models.ForeignKey('CustomIssuePriority', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssuePriorityActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('current').filter(deleted=None)


class CustomIssuePriority(core_models.CoreModel):
    """
    Custom issue priority model.

    Parameters:
        current (CustomIssuePriorityData): Data about the custom issue priority.
    """

    class Meta:
        ordering = ['current__name']

    active_objects = CustomIssuePriorityActiveManager()

    current = models.OneToOneField(CustomIssuePriorityData, on_delete=models.CASCADE)
