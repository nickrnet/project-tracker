from django.db import models

from core.models import core as core_models


class ComponentData(core_models.CoreModel):
    """
    Data about a component.

    Parameters:
        component (Component): The Component this data is about.
        name (str): The name of the component.
        description (str): A description of the component.
        label (str): A label for the component.
        is_active (bool): Whether the component is active.
    """

    component = models.ForeignKey('Component', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    label = models.CharField(max_length=255, blank=True, null=True, default="")
    is_active = models.BooleanField(default=True)


class Component(core_models.CoreModel):
    """
    A component of a project.

    Parameters:
        current (ComponentData): The data about this component.
        project (Project): The project this component belongs to.
    """

    class Meta:
        ordering = ['current__name']

    current = models.OneToOneField(ComponentData, on_delete=models.CASCADE, related_name='current')
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.current.name
