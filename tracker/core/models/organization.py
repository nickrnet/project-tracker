import uuid

from django.db import models, transaction
from django.forms.models import model_to_dict
from django.utils import timezone

from phone_field import PhoneField

from core.models import core as core_models
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models
from project.models import project as project_models


# TODO: Roles like Administrator, etc.


class OrganizationData(core_models.CoreModel):
    """
    Information about an Organization, both past and present.
    """

    class Meta:
        ordering = ['-created_on', 'name']

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True, default="")
    responsible_party_email = models.EmailField(max_length=255)
    responsible_party_phone = PhoneField()
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, default="")
    postal_code = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255, default=timezone.get_default_timezone_name())

    is_paid = models.BooleanField(default=False)
    renewal_date = models.DateField(blank=True, null=True)
    number_users_allowed = models.IntegerField(default=5)


class OrganizationActiveManager(models.Manager):
    """
    Active Organizations are not deleted.
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class Organization(core_models.CoreModel):
    """
    An organization. The _real_ inforomation about an Organization is stored in `current` as OrganizationData.

    Every time a user or a git repository or a project is added to an organization, a new OrganizationData object is created and the `current` field is updated to reflect the new data.
    """

    class Meta:
        ordering = ['current__name']

    active_objects = OrganizationActiveManager()

    current = models.ForeignKey(OrganizationData, on_delete=models.CASCADE)

    # TODO: Activity Tracking for tracking changes to these things
    members = models.ManyToManyField(core_user_models.CoreUser, related_name='organizationmembers_set')
    git_repositories = models.ManyToManyField(git_repository_models.GitRepository, related_name='organizationgitrepositories_set')
    projects = models.ManyToManyField(project_models.Project, related_name='organizationprojects_set')

    def update_organization_data(self, user_id: uuid.UUID, new_organization_data: dict) -> 'Organization':
        """
        Updates an organization's data. This is a helper function to illustrate the use of `current` retention since we do not delete data.

        Args:
            user_id (uuid): The ID of the user updating the organization.
            organization_data (dictionary): The data to update in an organization.

        Returns:
            Organization: The updated organization.
        """

        with transaction.atomic():
            current_organization_data = model_to_dict(self.current)
            current_organization_data.update(new_organization_data)
            current_organization_data['created_by_id'] = user_id
            new_organization_data = OrganizationData.objects.create(**current_organization_data)
            new_organization_data.save()
            self.current = new_organization_data
            self.save()

        return self

    def __str__(self) -> str:
        return self.current.name
