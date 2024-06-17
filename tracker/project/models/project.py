from django.db import models
from django.utils import timezone

from core.models import core as core_models
from core.models import user as user_models
from . import git_repository as git_repository_models


class Project(core_models.CoreModel):
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'git_repository']

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    git_repository = models.OneToOneField(git_repository_models.GitRepository, on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField(user_models.CoreUser, related_name='projectusers_set')
