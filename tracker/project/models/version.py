from django.db import models

from core.models import core as core_models


class VersionData(core_models.CoreModel):
    """
    Contains data about a Version.

    Parameters:
        version (Version): The version this data is about.
        name (str): The name of the version.
        description (str): A description of the version.
        label (str): The label of the version.
        release_date (date): The release date of the version.
        is_active (bool): Whether the version is active.
    """

    version = models.ForeignKey('Version', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    label = models.CharField(max_length=255)
    release_date = models.DateField(blank=True, null=True, default="")
    is_active = models.BooleanField(default=True)


class VersionActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('current').filter(deleted=None)


class Version(core_models.CoreModel):
    """
    A Version.

    Parameters:
       current (VersionData): Information about the version.
       project (Project): The project associated with the version.
    """

    class Meta:
        ordering = ['current__name']

    active_objects = VersionActiveManager()

    current = models.OneToOneField(VersionData, on_delete=models.CASCADE, related_name='version_data')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.current.name
