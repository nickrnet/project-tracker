from django.db import models
from django.utils import timezone

from phone_field import PhoneField

from core.models import core as core_models
from core.models import user as core_user_models
from project.models import git_repository as git_repository_models
from project.models import project as project_models


class OrganizationData(core_models.CoreModel):

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

    members = models.ManyToManyField(core_user_models.CoreUser, related_name='organizationmembers_set')
    repositories = models.ManyToManyField(git_repository_models.GitRepository, related_name='organizationrepositories_set')
    projects = models.ManyToManyField(project_models.Project, related_name='organizationprojects_set')


class OrganizationActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class Organization(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = OrganizationActiveManager()

    current = models.OneToOneField(OrganizationData, on_delete=models.CASCADE)
