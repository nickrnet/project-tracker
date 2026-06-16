import uuid

from django.db import models, transaction
from django.forms.models import model_to_dict
from django.utils import timezone

from core.models import core as core_models
from core.models import user as core_user_models
from . import git_repository as git_repository_models


class ProjectLabelData(core_models.CoreModel):
    """
    Data about a project label.

    Parameters:
        project_label (ProjectLabel): The project label this data is about.
        label (str): The label of the project label.
        description (str): The description of the project label.
        color (str): The color for the project label.
    """

    project_label = models.ForeignKey('ProjectLabel', on_delete=models.CASCADE, blank=True, null=True)

    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    color = models.CharField(max_length=7, default="#000000")


class ProjectLabel(core_models.CoreModel):
    """
    A project label.

    Parameters:
        current (ProjectLabelData): The data for this project label.
    """

    current = models.OneToOneField(ProjectLabelData, on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.current.label


class ProjectData(core_models.CoreModel):
    """
    Contains data about a project.

    Parameters:
        project (Project): The project this data is about.
        name (str): The name of the project.
        description (str): The description of the project.
        start_date (date): The start date of the project.
        end_date (date): The end date of the project.
        is_active (bool): Whether the project is active.
        is_private (bool): Whether the project is private.
    """

    project = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)


class ProjectActiveManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().select_related('current', 'label').filter(deleted=None).filter(current__is_active=True)


class Project(core_models.CoreModel):
    """
    A Project.

    Parameters:
        current (ProjectData): The current data of the project.
        label (ProjectLabel): The label of the project.
        git_repositories (list[GitRepository]): The Git repositories associated with the project.
        users (list[CoreUser]): The users associated with the project.
    """

    class Meta:
        ordering = ['current__name']

    active_objects = ProjectActiveManager()

    current = models.OneToOneField(ProjectData, on_delete=models.CASCADE, related_name='project_data')

    label = models.OneToOneField(ProjectLabel, on_delete=models.CASCADE, blank=True, null=True, related_name='projects_by_label')
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

        with transaction.atomic():
            self.users.set(users)
            self.save()

        return self

    def generate_label(self) -> str:
        """
        A helper method to generate a project label based on the project's name.

        Returns:
            str: A hyphenated label based on the project's name.
        """

        return "-".join(self.current.name.split()).lower()

    def update_project_label(self, user_id: uuid.UUID, new_project_label: ProjectLabel) -> 'Project':
        """
        A helper method to update a project label.

        Args:
            user_id (uuid.UUID): The logged in user that is updating the label.
            new_project_label (ProjectLabel): The new project label data.

        Returns:
            project (Project): The updated project.
        """

        new_project_label_data = ProjectLabelData.objects.create(created_by_id=user_id, **new_project_label.get('current'))
        new_project_label = ProjectLabel.objects.create(created_by_id=user_id, current=new_project_label_data, project=self)
        new_project_label_data.project_label = new_project_label
        new_project_label_data.save()
        self.label = new_project_label
        self.save()

        return self

    def list_users(self) -> list:
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
        return core_user_models.CoreUser.active_objects.filter(id__in=user_ids)

    def list_issues(self) -> list:
        """
        A helper method to list the project's issues.

        Returns:
            issues (list): The list of issues for the project.
        """

        issues = self.issue_set.all()
        return issues

    def __str__(self):
        potential_names = []
        if self.current.name:
            potential_names.append(self.current.name)
        if self.label:
            potential_names.append(f"- ({self.label})")
        return ' '.join(potential_names)
