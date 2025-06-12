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
    current = models.ForeignKey('ProjectLabelData', on_delete=models.CASCADE)


class ProjectData(core_models.CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
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

    label = models.ForeignKey(ProjectLabel, on_delete=models.CASCADE, blank=True, null=True)
    git_repositories = models.ManyToManyField(git_repository_models.GitRepository)
    users = models.ManyToManyField('core.CoreUser')

    def update_project_data(self, user_id: uuid.UUID, project_data: ProjectData) -> 'Project':
        """
        Updates a project's data. This is a helper function to illustrate the use of `current` retention since we do not delete data.

        Args:
            user_id (uuid): The UUID of the user updating the project.
            project_data (dictionary): The data to update in a project.

        Returns:
            Project: The updated project.
        """

        with transaction.atomic():
            current_project_data = model_to_dict(self.current)

            new_project_data = {}
            new_project_data['created_by_id'] = user_id
            new_project_data['name'] = project_data.get('name', current_project_data.get('name', ''))
            new_project_data['description'] = project_data.get('description', current_project_data.get('description', ''))
            new_project_data['start_date'] = project_data.get('start_date', current_project_data.get('start_date', ''))
            new_project_data['end_date'] = project_data.get('end_date', current_project_data.get('end_date', ''))
            new_project_data['is_active'] = project_data.get('is_active', current_project_data.get('is_active', ''))
            new_project_data['is_private'] = project_data.get('is_private', current_project_data.get('is_private', ''))
            new_project_data = ProjectData(**new_project_data)

            new_project_data.save()
            self.current = new_project_data
            self.save()
        return self
    
    def update_git_repositories(self, git_repositories: list) -> 'Project':
        """
        A helper method to update the git repositories that may use this project.

        Args:
            git_repositories (list): A list of UUIDs of git repository objects to be shown with this project.

        Returns:
            Project: The updated project.
        """
        self.git_repositories.set(git_repositories)
        self.save()

        return self
    
    def update_users(self, users: list) -> 'Project':
        """
        A helper method to update the users that have access to this project.

        Args:
            users (list): A list of UUIDs of users to be shown with this project.

        Returns:
            Project: The updated project
        """

        self.users.set(users)
        self.save()

        return self

    def generate_label(self):
        """
        A helper method to generate a project label based on the project's name.

        Returns:
            str: A hyphenated label based on the project's name.
        """

        return "-".join(self.current.name.split()).lower()
    
    def update_project_label(self, user_id: uuid.UUID, new_project_label: ProjectLabel):
        """
        A helper method to update a project label.

        Args:
            user_id (uuid.UUID): The logged in user that is updating the label.
            new_project_label (ProjectLabel): The new project label, containing ProjectLabelData.

        Returns:
            project (Project): The updated project.
        """
        
        new_project_label_data = ProjectLabelData(created_by_id=user_id, **new_project_label.get('current'))
        new_project_label_data.save()
        new_label = ProjectLabel(created_by_id=user_id, current=new_project_label_data)
        new_label.save()
        self.label = new_label
        self.save()

        return self

    def list_users(self):
        """
        A helper method to list the users that could potentially access this project. Based on the logged in user's organization and this project.

        Returns:
            users (list): The list of users.
        """

        # Get unique users from owning organization and this project
        organization_data = self.organizationprojects_set.first()
        if organization_data:
            organization_users = organization_data.members.values_list('id', flat=True)
        else:
            organization_users = []
        project_users = self.users.values_list('id', flat=True)
        # Combine the user IDs and get distinct users
        user_ids = set(organization_users).union(set(project_users))
        return core_user_models.CoreUser.objects.filter(id__in=user_ids)

    def list_issues(self):
        """
        A helper method to list the project's issues.

        Returns:
            issues (list): The list of issues for the project.
        """

        # Get the issues from the issue data for the project - there could be a lot of issue data for a single issue so we have to pare it down with a set, could try distinct here for performance when needed.
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
