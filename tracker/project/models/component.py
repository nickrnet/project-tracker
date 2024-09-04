from django.db import models

from core.models import core as core_models


class ComponentData(core_models.CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)


class Component(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    current = models.ForeignKey(ComponentData, on_delete=models.CASCADE)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.current.name
