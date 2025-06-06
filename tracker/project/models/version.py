from django.db import models

from core.models import core as core_models


class VersionData(core_models.CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    label = models.CharField(max_length=255)
    release_date = models.DateField(blank=True, null=True, default="")
    is_active = models.BooleanField(default=True)


class VersionActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class Version(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = VersionActiveManager()

    current = models.ForeignKey(VersionData, on_delete=models.CASCADE)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.current.name
