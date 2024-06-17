from django.db import models

from core.models import core as core_models


class GitRepository(core_models.CoreModel):
    class Meta:
        unique_together = ['name', 'url']

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
