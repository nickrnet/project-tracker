from django.db import models
from django.utils import timezone

from core.models import core as core_models
from core.models import user as core_user_models
from . import git_repository as git_repository_models


class ProjectData(core_models.CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    label = models.CharField(max_length=255, blank=True, null=True, default="")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    def generate_label(self):
        return "-".join(self.name.split()).lower()


class ProjectLabelName(core_models.CoreModel):
    class Meta:
        unique_together = ['name']

    name = models.CharField(max_length=255)


class ProjectLabelData(core_models.CoreModel):
    name = models.ForeignKey(ProjectLabelName, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, default="")
    color = models.CharField(max_length=7, default="#000000")


class ProjectLabel(core_models.CoreModel):
    current = models.OneToOneField('ProjectLabelData', on_delete=models.CASCADE)


class ProjectActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None).filter(current__is_active=True)


class Project(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = ProjectActiveManager()

    current = models.OneToOneField(ProjectData, on_delete=models.CASCADE)
    label = models.ForeignKey(ProjectLabel, on_delete=models.CASCADE, blank=True, null=True, default="")
    git_repositories = models.ManyToManyField(git_repository_models.GitRepository)
    users = models.ManyToManyField('core.CoreUser')

    def list_users(self, logged_in_user):
        # Get unique users from owned organizations and projects
        organization_users = logged_in_user.organizationmembers_set.first().members.values_list('id', flat=True)
        project_users = logged_in_user.list_projects().values_list('users', flat=True)
        # Managing users of an organization is a different view
        # Combine the user IDs and get distinct users
        user_ids = set(organization_users).union(set(project_users))
        return core_user_models.CoreUser.objects.filter(id__in=user_ids)

    def __str__(self):
        potential_names = []
        if self.current.name:
            potential_names.append(self.current.name)
        if self.current.label:
            potential_names.append(f"- ({self.current.label})")
        return self.current.name
