import uuid

from django.db import models, transaction
from django.forms.models import model_to_dict
from django.utils import timezone

from core.models import core as core_models
from core.models import user as core_user_models
from . import git_repository as git_repository_models
from . import issue as issue_models


class ProjectLabelData(core_models.CoreModel):
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    color = models.CharField(max_length=7, default="#000000")


class ProjectLabel(core_models.CoreModel):
    current = models.OneToOneField('ProjectLabelData', on_delete=models.CASCADE)


class ProjectData(core_models.CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)

    label = models.ForeignKey(ProjectLabel, on_delete=models.CASCADE, blank=True, null=True)
    git_repositories = models.ManyToManyField(git_repository_models.GitRepository)
    users = models.ManyToManyField('core.CoreUser')

    def generate_label(self):
        return "-".join(self.name.split()).lower()


class ProjectActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None).filter(current__is_active=True)


class Project(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = ProjectActiveManager()

    current = models.OneToOneField(ProjectData, on_delete=models.CASCADE)

    def update_project_data(self, user_id: uuid.UUID, project_data: dict) -> 'Project':
        """
        Updates a project's data. This is a helper function to illustrate the use of `current` retention since we do not delete data.

        Args:
            user_id (uuid): The UUID of the user updating the project.
            data (dictionary): The data to update in a project.

        Returns:
            Project: The updated project.
        """

        with transaction.atomic():
            current_project_data = model_to_dict(self.current)
            # ManyToMany fields need to be handled separately
            current_project_git_repositories = current_project_data.pop('git_repositories', [])
            current_project_users = current_project_data.pop('users', [])
            new_project_git_repositories = project_data.pop('git_repositories', [])
            new_project_users = project_data.pop('users', [])
            # How much logic should be here for nested current fields? Should they be in their own classes?
            # project_data could be like:
            # {
            #     'name': 'New Project Name',
            #     'description': 'New Project Description',
            #     'is_active': True,
            #  ...
            #     'label': {
            #         'current': {
            #             'label': 'new-project-label',
            #             'description': 'New Project Label Description',
            #             'color': '#000000',
            #         },
            #     },
            #  ...
            # }
            if self.current.label:
                existing_label = ProjectLabel.objects.filter(id=self.current.label.id).first()
            else:
                existing_label = None
            new_label = project_data.pop('label', None)
            if new_label and new_label.get('current', None) and new_label.get('current').get('label', None):
                new_label_data = ProjectLabelData(created_by_id=user_id, **new_label.get('current'))
                new_label_data.save()
                if existing_label:
                    existing_label.current = new_label_data
                    existing_label.save()
                else:
                    existing_label = ProjectLabel(created_by_id=user_id, current=new_label_data)
                    existing_label.save()

            current_project_data.update(project_data)
            current_project_data['created_by_id'] = user_id

            new_project_data = ProjectData(**current_project_data)
            new_project_data.save()
            if new_label and new_label_data:
                new_project_data.label = existing_label
            # Handle ManyToMany fields
            # TODO: Handle removing things from ManyToMany fields
            for git_repository in current_project_git_repositories:
                new_project_data.git_repositories.add(git_repository)
            for git_repository in new_project_git_repositories:
                new_project_data.git_repositories.add(git_repository)
            for user in current_project_users:
                new_project_data.users.add(user)
            for user in new_project_users:
                new_project_data.users.add(user)

            new_project_data.save()
            self.current = new_project_data
            self.save()
        return self

    def list_users(self, logged_in_user: core_user_models.CoreUser):
        # Get unique users from owned organizations and projects
        if logged_in_user.organizationmembers_set.exists():
            organization_users = logged_in_user.organizationmembers_set.first().members.values_list('id', flat=True)
        else:
            organization_users = []
        project_users = logged_in_user.list_projects().values_list('current__users', flat=True)
        # Managing users of an organization is a different query
        # Combine the user IDs and get distinct users
        user_ids = set(organization_users).union(set(project_users))
        return core_user_models.CoreUser.objects.filter(id__in=user_ids)

    def list_issues(self):
        # Get the issue data for the project
        issue_ids = set()
        issue_datas = self.issuedata_set.values_list('issue', flat=True).filter(project=self)
        issue_ids.update(issue_datas)
        return issue_models.Issue.objects.filter(id__in=issue_ids)

    def __str__(self):
        potential_names = []
        if self.current.name:
            potential_names.append(self.current.name)
        if self.current.label:
            potential_names.append(f"- ({self.current.label})")
        return self.current.name
