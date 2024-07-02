from django.db import models

from core.models import core as core_models


class GitRepositoryActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class GitRepository(core_models.CoreModel):
    class Meta:
        ordering = ['name', 'url']
        unique_together = ['name', 'url']

    active_objects = GitRepositoryActiveManager()

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
