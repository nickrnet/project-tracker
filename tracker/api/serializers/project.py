from rest_framework import serializers

from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.issue_type import BuiltInIssueType, CustomIssueType
from project.models.issue import Issue
from project.models.priority import BuiltInIssuePriority, CustomIssuePriority, CustomIssuePriorityData
from project.models.project import Project, ProjectData
from project.models.status import BuiltInIssueStatus, CustomIssueStatus, CustomIssueStatusData
from project.models.severity import BuiltInIssueSeverity, CustomIssueSeverity, CustomIssueSeverityData
from project.models.component import Component, ComponentData
from project.models.version import Version, VersionData

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


class BuiltInIssueSeveritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BuiltInIssueSeverity
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


class ComponentDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponentData
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'name',
            'description',
            'label',
            'is_active'
            ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class CustomIssuePriorityDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssuePriorityData
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
    current = CustomIssuePriorityDataSerializer()


class CustomIssueSeverityDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueSeverityData
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


class CustomIssueSeveritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueSeverity
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current'
            ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()
    current = CustomIssueSeverityDataSerializer()


class CustomIssueStatusDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomIssueStatusData
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
    current = CustomIssueStatusDataSerializer()


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
    current = CustomIssueTypeDataSerializer()


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
            ]

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
    current = IssueDataSerializer()


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
            'git_repositories',
            'users',
            ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()
    git_repositories = GitRepositorySerializer(many=True)
    users = CoreUserSerializer(many=True)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current',
            ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()
    current = ProjectDataSerializer()


class VersionDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VersionData
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'name',
            'description',
            'release_date',
            'is_active',
            ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class VersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Version
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current',
            'project'
            ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()
    current = VersionDataSerializer()
    project = ProjectSerializer()


class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Component
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current',
            'project'
            ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()
    current = ComponentDataSerializer()
    project = ProjectSerializer()
