from django.db import models

from core.models import core as core_models


class GitRepositoryData(core_models.CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    url = models.CharField(max_length=255, blank=True, null=True, default="")


class GitRepositoryActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class GitRepository(core_models.CoreModel):
    # TODO: GitHub, GitLab, BitBucket, etc. integrations

    class Meta:
        ordering = ['current__name', 'current__url']

    active_objects = GitRepositoryActiveManager()
    current = models.ForeignKey(GitRepositoryData, on_delete=models.CASCADE)

    def __str__(self):
        potential_names = []
        if self.current.name:
            potential_names.append(self.current.name)
        if self.current.url:
            potential_names.append(f"- ({self.current.url})")
        return " ".join(potential_names)
