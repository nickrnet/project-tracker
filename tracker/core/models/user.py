import pytz

from django.contrib.auth.models import User as DjangoUser
from django.db import models, transaction
from phone_field import PhoneField

# DO NOT IMPORT OTHER TRACKER APP MODELS HERE, IT WILL CAUSE A CIRCULAR IMPORT SINCE ALL MODELS IMPORT CORE.COREUSER and/or CORE.COREMODEL
# Use the string reference to the model here or import directly in helper functions instead to lazy-load it - See CoreUser.list_projects() for an example
from . import core as core_models


TIMEZONE_CHOICES = tuple((tz, tz) for tz in pytz.all_timezones)


class CoreUserData(core_models.CoreModel):
    """
    Demographic information about a user.
    """

    name_prefix = models.CharField(max_length=255, blank=True, null=True, default="")
    first_name = models.CharField(max_length=255, blank=True, null=True, default="")
    middle_name = models.CharField(max_length=255, blank=True, null=True, default="")
    last_name = models.CharField(max_length=255, blank=True, null=True, default="")
    name_suffix = models.CharField(max_length=255, blank=True, null=True, default="")
    email = models.EmailField(max_length=255)
    secondary_email = models.EmailField(max_length=255, blank=True, null=True, default="")
    home_phone = PhoneField(blank=True, null=True)
    mobile_phone = PhoneField(blank=True, null=True)
    work_phone = PhoneField(blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True, default="")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, default="")
    postal_code = models.CharField(max_length=255, blank=True, null=True, default="")
    city = models.CharField(max_length=255, blank=True, null=True, default="")
    state = models.CharField(max_length=255, blank=True, null=True, default="")
    country = models.CharField(max_length=255, blank=True, null=True, default="")
    timezone = models.CharField(max_length=255, default='UTC', choices=TIMEZONE_CHOICES)


class CoreUserActiveManager(models.Manager):
    """
    Active CoreUsers are ones that are not deleted.
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class CoreUserManager(core_models.CoreModelManager):
    """
    General helper methods for managing CoreUsers, active or deleted.
    """

    def get_or_create_api_user(self):
        """
        Creates an API user if it does not exist, primarily for Web tasks.

        Returns:
            api_user (CoreUser): The API user.
        """

        try:
            api_user = CoreUser.objects.get(pk='75af4764-0f94-49f2-a6dc-3dbfe1b577f9')
        except CoreUser.DoesNotExist:
            with transaction.atomic():
                api_user = CoreUser(
                    id='75af4764-0f94-49f2-a6dc-3dbfe1b577f9',
                    created_by_id='75af4764-0f94-49f2-a6dc-3dbfe1b577f9',
                    )
                api_user.save()
                api_user_data = CoreUserData(
                    id='373f414f-9692-4e5c-92f2-5781dbad5c04',
                    created_by_id='75af4764-0f94-49f2-a6dc-3dbfe1b577f9',
                    first_name='API',
                    last_name='USER',
                    address_line_1='',
                    address_line_2='',
                    city='',
                    state='',
                    country='',
                    postal_code=0,
                    )
                api_user_data.save()
                api_user.current = api_user_data
                api_user.save()

        return api_user

    def get_or_create_system_user(self):
        """
        Creates a system user if it does not exist, primarily for setup and system tasks.

        Returns:
            system_user (CoreUser): The system user.
        """

        try:
            system_user = CoreUser.objects.get(pk='45407f07-21e9-42ba-8c39-03b57767fe76')
        except CoreUser.DoesNotExist:
            with transaction.atomic():
                system_user = CoreUser(
                    id='45407f07-21e9-42ba-8c39-03b57767fe76',
                    created_by_id='45407f07-21e9-42ba-8c39-03b57767fe76',
                    )
                system_user.save()
                system_user_data = CoreUserData(
                    id='02e94188-5b8e-494a-922c-bc6ed2ffcfc4',
                    created_by_id='45407f07-21e9-42ba-8c39-03b57767fe76',
                    first_name='SYSTEM',
                    last_name='USER',
                    address_line_1='',
                    address_line_2='',
                    city='',
                    state='',
                    country='',
                    postal_code=0,
                    )
                system_user_data.save()
                system_user.current = system_user_data
                system_user.save()

        return system_user

    def create_core_user_from_web(self, request_data: dict) -> 'CoreUser':
        """
        Takes a flat dictionary and creates a CoreUser and CoreUserData object.

        Args:
            request_data (dict): Probaby a JSON payload from a POST request.

        Returns:
            new_user (CoreUser): The new user that was created.
        """

        with transaction.atomic():
            api_user = CoreUser.objects.get_or_create_api_user()

            django_user = DjangoUser.objects.create_user(
                username=request_data.get('email'),
                email=request_data.get('email'),
                password=request_data.get('password')
                )

            core_user_data = CoreUserData(
                created_by_id=api_user.id,
                first_name=request_data.get('first_name', ''),
                last_name=request_data.get('last_name', ''),
                email=request_data.get('email'),
                secondary_email=request_data.get('secondary_email', ''),
                home_phone=request_data.get('home_phone', ''),
                mobile_phone=request_data.get('mobile_phone', ''),
                work_phone=request_data.get('work_phone', ''),
                address_line_1=request_data.get('address_line_1', ''),
                address_line_2=request_data.get('address_line_2', ''),
                postal_code=request_data.get('postal_code', ''),
                city=request_data.get('city', ''),
                state=request_data.get('state', ''),
                country=request_data.get('country', ''),
                timezone=request_data.get('timezone', ''),
                )
            core_user_data.save()

            new_user = CoreUser(
                created_by_id=api_user.id,
                current=core_user_data,
                user=django_user
                )
            new_user.save()

            return new_user


class CoreUser(core_models.CoreModel, core_models.CoreModelActiveManager, core_models.CoreModelManager):
    """
    A user of the system. The _real_ inforamation about a user is stored in `current` as CoreUserData.
    Every time a user is updated, a new CoreUserData object is created and the `current` field is updated to reflect the new data.
    The `user` field is a Django User object that is used for authentication and authorization.
    The `current` field is a OneToOneField to CoreUserData, which contains the user's demographic information.
    """

    class Meta:
        ordering = ['current__last_name', 'current__email']

    active_objects = CoreUserActiveManager()
    objects = CoreUserManager()

    current = models.OneToOneField(CoreUserData, on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, blank=True, null=True, related_name='django_user')

    def deactivate_login(self) -> None:
        """
        Deactivates a user's login and disaables login to the webapp/api.
        """

        self.user.is_active = False
        self.user.save()

    def list_projects(self):
        """
        Get all projects the user is a member of or owns.

        Returns:
            projects (list): The projects the user is a member of or owns.
        """

        from project.models import project
        # Get projects from organization memberships and projects the user owns
        organization_projects = self.organizationmembers_set.values_list('projects', flat=True).exclude(projects__isnull=True)
        user_projects = self.projectdata_set.values_list('project', flat=True)
        # Combine the project IDs and get distinct ones
        project_ids = set(organization_projects).union(set(user_projects))
        projects = project.Project.objects.filter(id__in=project_ids)
        # breakpoint()
        return projects

    def list_git_repositories(self):
        """
        A helper method to get all git repositories the user can see or owns.

        Returns:
            repositories (list): All git repositories the user can see.
        """

        from project.models import project as project_models
        from project.models import git_repository as git_repository_models
        # Get repositories from organizations and projects the user can see
        organization_repositoriess = self.organizationmembers_set.values_list('git_repositories', flat=True).exclude(git_repositories__isnull=True)
        project_ids = set()
        project_datas = self.projectdata_set.values_list('project', flat=True)
        project_ids.update(project_datas)
        project_repositories = project_models.Project.objects.filter(id__in=project_ids).values_list('current__git_repositories', flat=True)
        user_repositories = git_repository_models.GitRepository.objects.filter(created_by=self).values_list('id', flat=True)
        # Combine the repository IDs and get distinct ones
        repository_ids = set(organization_repositoriess).union(set(project_repositories)).union(set(user_repositories))
        repositories = git_repository_models.GitRepository.objects.filter(id__in=repository_ids)
        return repositories

    def list_issues(self):
        """
        Get all issues the user is watching, assigned to, etc.

        Returns:
            issues (list): The issues the user is watching, assigned to, etc.
        """

        from project.models import issue as issue_models
        # TODO: Add issues watching, assigned to, etc.
        user_projects = self.list_projects()
        personal_issues = self.issue_created_by.values_list('id', flat=True)
        issue_ids = set()
        for project in user_projects:
            issue_ids = set(issue_ids).union(set(project.list_issues().values_list('id', flat=True)))
        issue_ids = set(issue_ids).union(set(personal_issues))
        issues = issue_models.Issue.objects.filter(id__in=issue_ids)
        return issues

    def list_organizations(self):
        """
        A helper method to get all organiations the user is a member of, etc.

        Returns:
            organizations (list): The organizations the user is a member of, etc.
        """

        from core.models import organization as core_organization_models

        organization_data_ids = set()
        organization_datas = self.organizationmembers_set.all()
        organization_data_ids.update(organization_datas.values_list('organization', flat=True))
        organizations = core_organization_models.Organization.objects.filter(id__in=organization_data_ids)

        return organizations

    def __str__(self):
        potential_names = []
        if self.current.first_name:
            potential_names.append(self.current.first_name)
        if self.current.last_name:
            potential_names.append(self.current.last_name)
        potential_names.append(f"({self.current.email})")
        return ' '.join(potential_names)


class UserLogin(core_models.CoreModel):
    """
    A record of a user's login to the webapp or API.
    """

    class Meta:
        ordering = ['-login_time']

    user = models.ForeignKey(CoreUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    x_forwarded_for = models.GenericIPAddressField(blank=True, null=True)
    remote_addr = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True, default="")
    session_key = models.CharField(max_length=255, blank=True, null=True, default="")


class UserLogout(core_models.CoreModel):
    """
    A record of a user's logout from the webapp or API.
    """

    class Meta:
        ordering = ['-logout_time']

    user = models.ForeignKey(CoreUser, on_delete=models.CASCADE)
    logout_time = models.DateTimeField(auto_now_add=True)
    x_forwarded_for = models.GenericIPAddressField(blank=True, null=True)
    remote_addr = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True, default="")
    session_key = models.CharField(max_length=255, blank=True, null=True, default="")
