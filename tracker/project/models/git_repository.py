from django.db import models

from core.models import core as core_models


class GitRepositoryData(core_models.CoreModel):
    """
    Contains data about a Git repository.

    Parameters:
        git_repository (GitRepository): The Git repository this data is about.
        name (str): The name of the Git repository.
        description (str): A description of the Git repository.
        url (str): The URL to the Git repository.
    """

    git_repository = models.ForeignKey('GitRepository', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    url = models.CharField(max_length=255, blank=True, null=True, default="")


class GitRepositoryActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class GitRepository(core_models.CoreModel):
    """
    A Git repository.

    Parameters:
        current (GitRepositoryData): Data about the Git repository.
    """

    # TODO: GitHub, GitLab, BitBucket, etc. integrations

    class Meta:
        ordering = ['current__name', 'current__url']

    active_objects = GitRepositoryActiveManager()

    current = models.OneToOneField(GitRepositoryData, on_delete=models.CASCADE)

    def __str__(self):
        potential_names = [self.current.name]
        if self.current.url:
            potential_names.append(f"- ({self.current.url})")
        return " ".join(potential_names)
