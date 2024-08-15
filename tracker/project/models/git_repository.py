from django.db import models

from core.models import core as core_models


class GitRepositoryData(core_models.CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)


class GitRepositoryActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class GitRepository(core_models.CoreModel):
    class Meta:
        ordering = ['current__name', 'current__url']

    active_objects = GitRepositoryActiveManager()
    current = models.OneToOneField(GitRepositoryData, on_delete=models.CASCADE)
