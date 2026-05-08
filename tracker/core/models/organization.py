import uuid

from django.db import models, transaction
from django.forms.models import model_to_dict
from django.utils import timezone

from phone_field import PhoneField

from core.models import core as core_models
from core.models import user as core_user_models
from subscription.models import organization as subscription_organization_models
from project.models import git_repository as git_repository_models
from project.models import project as project_models


# TODO: Roles like Administrator, etc.


class OrganizationData(core_models.CoreModel):
    """
    Information about an Organization.

    Parameters:
        name (str): The name of the organization.
        description (str): Optional: A description of the organization.
        responsible_party_email (str): The email of the responsible party for the organization.
        responsible_party_phone (str): The phone number of the responsible party for the organization.
        address_line_1 (str): The first line of the organization's address.
        address_line_2 (str): Optional: The second line of the organization's address.
        postal_code (str): The postal code of the organization's address.
        city (str): The city of the organization's address.
        state (str): The state of the organization's address.
        country (str): The country of the organization's address.
        timezone (str): Optional: The timezone of the organization.
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


class OrganizationActiveManager(models.Manager):
    """
    Active Organizations are ones that are not deleted.
    """

    def get_queryset(self):
        return super().get_queryset().select_related('current', 'subscription').filter(deleted=None)


class Organization(core_models.CoreModel):
    """
    An organization. The _real_ inforomation about an Organization is stored in `current` as OrganizationData.

    Every time a user updates information about an organization, a new OrganizationData object is created and the `current` field is updated to reflect the new data.

    Parameters:
        current (OrganizationData): The current data for the organization. This is a foreign key to the OrganizationData model, which contains all of the information about the organization. This allows us to keep a history of changes to the organization's data without actually deleting any data.
        subscription (OrganizationSubscription): Optional:The subscription that the organization is currently on. This is a foreign key to the OrganizationSubscription model, which contains information about the subscription that the organization is currently on.
        members (list[CoreUser]): The users that are members of this organization. This is a many-to-many relationship with the CoreUser model, which allows us to easily manage the users that are members of this organization.
        member_invites (list[OrganizationInvite]): The invites that have been sent to users to join this organization. This is a many-to-many relationship with the OrganizationInvite model, which allows us to easily manage the invites that have been sent to users to join this organization.
        git_repositories (list[GitRepository]): The git repositories that are associated with this organization. This is a many-to-many relationship with the GitRepository model, which allows us to easily manage the git repositories that are associated with this organization.
        projects (list[Project]): The projects that are associated with this organization. This is a many-to-many relationship with the Project model, which allows us to easily manage the projects that are associated with this organization.
    """

    class Meta:
        ordering = ['current__name']

    active_objects = OrganizationActiveManager()

    current = models.ForeignKey(OrganizationData, on_delete=models.CASCADE)

    # TODO: Activity Tracking for tracking changes to these things
    subscription = models.ForeignKey(subscription_organization_models.OrganizationSubscription, on_delete=models.SET_NULL, blank=True, null=True)
    members = models.ManyToManyField(core_user_models.CoreUser, related_name='organizationmembers_set')
    member_invites = models.ManyToManyField('OrganizationInvite', related_name='organizationmemberinvite_set')
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
            current_organization_data['created_on'] = timezone.now()
            new_organization_data = OrganizationData.objects.create(**current_organization_data)
            new_organization_data.save()
            self.current = new_organization_data
            self.save()

        return self

    def update_members(self, user_ids: list[str]) -> 'Organization':
        """
        A helper method to update the users that have access to this organization.

        Args:
            user_ids (list[str]): A list of UUIDs of users to be associated with this organization.

        Returns:
            Organization: The updated organization.
        """

        with transaction.atomic():
            self.members.set(user_ids)
            self.save()

        return self

    def __str__(self) -> str:
        return self.current.name

    def get_subscription(self):
        """
        Gets the subscription that the organization is currently on.

        Returns:
            OrganizationSubscription: The subscription that the organization is currently on.
        """

        return self.subscription
