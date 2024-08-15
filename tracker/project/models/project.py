from django.db import models
from django.utils import timezone

from core.models import core as core_models
from core.models import user as core_user_models
from . import git_repository as git_repository_models
from . import issue as issue_models


class ProjectData(core_models.CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    label = models.CharField(max_length=255, blank=True, null=True, default="")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    git_repository = models.ForeignKey(git_repository_models.GitRepository, on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField(core_user_models.CoreUser)
    issues = models.ManyToManyField(issue_models.Issue)


class ProjectActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class Project(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = ProjectActiveManager()

    current = models.ForeignKey(ProjectData, on_delete=models.CASCADE)
