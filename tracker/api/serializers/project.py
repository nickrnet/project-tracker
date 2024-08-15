from rest_framework import serializers

from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.issue_type import BuiltInIssueType, CustomIssueType
from project.models.issue import Issue
from project.models.priority import BuiltInIssuePriority, CustomIssuePriority
from project.models.project import Project
from project.models.status import BuiltInIssueStatus, CustomIssueStatus

from .core import DeletedModelDataSerializer


class GitRepositoryDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GitRepositoryData
        fields = ['id', 'created_by', 'name', 'description', 'url', 'deleted']

    deleted = DeletedModelDataSerializer()


class GitRepositorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GitRepository
        fields = ['id', 'created_by', 'current', 'deleted']

    deleted = DeletedModelDataSerializer()


class BuiltInIssuePrioritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BuiltInIssuePriority
        fields = ['id', 'created_by', 'name', 'description', 'deleted']

    deleted = DeletedModelDataSerializer()


class BuiltInIssueStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BuiltInIssueStatus
        fields = ['id', 'created_by', 'name', 'description', 'deleted']

    deleted = DeletedModelDataSerializer()


class BuiltInIssueTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BuiltInIssueType
        fields = ['id', 'created_by', 'type', 'description', 'deleted']

    deleted = DeletedModelDataSerializer()


class CustomIssuePriorityDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssuePriority
        fields = ['id', 'created_by', 'name', 'description', 'deleted']

    deleted = DeletedModelDataSerializer()


class CustomIssuePrioritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssuePriority
        fields = ['id', 'created_by', 'current', 'deleted']

    deleted = DeletedModelDataSerializer()


class CustomIssueStatusDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueStatus
        fields = ['id', 'created_by', 'name', 'description', 'deleted']

    deleted = DeletedModelDataSerializer()


class CustomIssueStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueStatus
        fields = ['id', 'created_by', 'current', 'deleted']

    deleted = DeletedModelDataSerializer()


class CustomIssueTypeDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueType
        fields = ['id', 'created_by', 'name', 'description', 'deleted']

    deleted = DeletedModelDataSerializer()


class CustomIssueTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueType
        fields = ['id', 'created_by', 'current', 'deleted']

    deleted = DeletedModelDataSerializer()


class IssueDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'created_by', 'summary', 'description', 'deleted']  # TODO: add all the issue fields

    deleted = DeletedModelDataSerializer()


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'created_by', 'current', 'deleted']  # TODO: add all the issue fields

    deleted = DeletedModelDataSerializer()


class ProjectDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'created_by', 'name', 'description', 'start_date', 'end_date', 'is_active', 'is_private', 'git_repository', 'users', 'deleted']

    deleted = DeletedModelDataSerializer()


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'created_by', 'current', 'deleted']

    deleted = DeletedModelDataSerializer()
