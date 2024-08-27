from rest_framework import serializers

from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.issue_type import BuiltInIssueType, CustomIssueType
from project.models.issue import Issue
from project.models.priority import BuiltInIssuePriority, CustomIssuePriority
from project.models.project import Project, ProjectData
from project.models.status import BuiltInIssueStatus, CustomIssueStatus

from .core import DeletedModelDataSerializer
from .user import CoreUserSerializer


class GitRepositoryDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GitRepositoryData
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'name',
            'description',
            'url'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class GitRepositorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GitRepository
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()
    current = GitRepositoryDataSerializer()


class BuiltInIssuePrioritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BuiltInIssuePriority
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'name',
            'description'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class BuiltInIssueStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BuiltInIssueStatus
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'name',
            'description'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class BuiltInIssueTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BuiltInIssueType
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'type',
            'description'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class CustomIssuePriorityDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssuePriority
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'name',
            'description'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class CustomIssuePrioritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssuePriority
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class CustomIssueStatusDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueStatus
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'name',
            'description'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class CustomIssueStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueStatus
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class CustomIssueTypeDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueType
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'name',
            'description'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class CustomIssueTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueType
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current'
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class IssueDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'summary',
            'description'
        ]  # TODO: add all the issue fields

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current'
        ]  # TODO: add all the issue fields

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class ProjectDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectData
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'name',
            'description',
            'start_date',
            'end_date',
            'is_active',
            'is_private',
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current',
            'git_repository',
            'users',
        ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()
    current = ProjectDataSerializer()
    git_repository = GitRepositorySerializer(many=True)
    users = CoreUserSerializer(many=True)
