from django.db import models
from django.utils import timezone

from core.models import core as core_models
from . import git_repository as git_repository_models


class ProjectData(core_models.CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    label = models.CharField(max_length=255, blank=True, null=True, default="")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)


class ProjectActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None).filter(current__is_active=True)


class Project(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = ProjectActiveManager()

    current = models.ForeignKey(ProjectData, on_delete=models.CASCADE)
    git_repositories = models.ManyToManyField(git_repository_models.GitRepository)
    users = models.ManyToManyField('core.CoreUser')

    def __str__(self):
        potential_names = []
        if self.current.name:
            potential_names.append(self.current.name)
        if self.current.label:
            potential_names.append(f"- ({self.current.label})")
        return self.current.name
