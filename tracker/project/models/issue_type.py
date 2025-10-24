from django.db import models

from core.models import core as core_models
from core.models import user as core_user_models


class BuiltInIssueTypeManager(models.Manager):
    def initialize_built_in_types(self):
        """
        Keep this synchronized with the BuiltInIssueType.IssueTypeChoices class.
        """
        built_in_types = [
            ('c166c9dc-f058-4fb7-99c3-eb2bc14a46ee', 'CHANGE_REQUEST', 'Change Request'),
            ('94e3841b-3c88-4273-9dd0-190aa5e7c8ea', 'PROBLEM', 'Problem'),
            ('d34e6879-e36c-4eb4-a9e5-b74800cebbed', 'INCIDENT', 'Incident'),
            ('b7c197df-723d-4687-b421-327b6fc2fcf8', 'SERVICE_REQUEST', 'Service Request'),
            ('849a2e5a-9920-47f8-8545-2546645995da', 'TEST', 'Test'),
            ('f83fe0be-6c55-47a4-b3e7-025db8e0c63d', 'IMPROVEMENT', 'Improvement'),
            ('218ffda9-4e5d-48a9-b90e-46ae759d80a3', 'ENHANCEMENT', 'Enhancement'),
            ('6d8e2776-ad44-41e1-bca6-6637cdeb70e6', 'QUESTION', 'Question'),
            ('a9198bed-0f07-4482-9687-6465d73a6910', 'PROPOSAL', 'Proposal'),
            ('ee0e2c17-99c2-40fb-ad28-1c23773d7d42', 'SPIKE', 'Spike'),
            ('00305b27-674b-469a-85b9-8a0b8cb63597', 'SUB_TASK', 'Sub-task'),
            ('c5da1c3c-ffa1-47fb-adbf-087a9d3527f9', 'TASK', 'Task'),
            ('33b0397f-3da9-4a91-ae48-5aa30d71dfe6', 'FEATURE', 'Feature'),
            ('bc3b8be9-0093-4826-80ba-e9874e8c05ca', 'STORY', 'Story'),
            ('8b4ba108-33b0-4481-bf52-ad891c7d9226', 'EPIC', 'Epic'),
            ('d43acc25-927a-4666-865f-2dd93b8418cb', 'DOCUMENTATION', 'Documentation'),
            ('b9a4b28c-b52d-42be-ad70-79f0e94fa462', 'BUG', 'Bug'),
            ]
        system_user = core_user_models.CoreUser.objects.get_or_create_system_user()

        for id, type, description in built_in_types:
            self.create(id=id, created_by=system_user, type=type, description=description)


class BuiltInIssueType(core_models.CoreModel):
    class Meta:
        ordering = ['type']
        unique_together = ['type', 'description']

    class IssueTypeChoices(models.TextChoices):
        """
        Keep this synchronized with the BuiltInIssueTypeManager.initialize_built_in_types method.
        """
        CHANGE_REQUEST = 'CHANGE_REQUEST', 'Change Request'
        PROBLEM = 'PROBLEM', 'Problem'
        INCIDENT = 'INCIDENT', 'Incident'
        SERVICE_REQUEST = 'SERVICE_REQUEST', 'Service Request'
        TEST = 'TEST', 'Test'
        IMPROVEMENT = 'IMPROVEMENT', 'Improvement'
        ENHANCEMENT = 'ENHANCEMENT', 'Enhancement'
        QUESTION = 'QUESTION', 'Question'
        PROPOSAL = 'PROPOSAL', 'Proposal'
        SPIKE = 'SPIKE', 'Spike'
        SUB_TASK = 'SUB_TASK', 'Sub-task'
        TASK = 'TASK', 'Task'
        FEATURE = 'FEATURE', 'Feature'
        STORY = 'STORY', 'Story'
        EPIC = 'EPIC', 'Epic'
        DOCUMENTATION = 'DOCUMENTATION', 'Documentation'
        BUG = 'BUG', 'Bug'

    objects = BuiltInIssueTypeManager()

    type = models.CharField(max_length=255, choices=IssueTypeChoices.choices)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssueTypeActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=None)


class CustomIssueTypeData(core_models.CoreModel):
    class Meta:
        ordering = ['name']

    active_objects = CustomIssueTypeActiveManager()

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, default="")


class CustomIssueType(core_models.CoreModel):
    class Meta:
        ordering = ['current__name']

    active_objects = CustomIssueTypeActiveManager()

    current = models.ForeignKey(CustomIssueTypeData, on_delete=models.CASCADE)
