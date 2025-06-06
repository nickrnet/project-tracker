from rest_framework import permissions, viewsets

# TODO: Break up this massive import list
from api.serializers.project import BuiltInIssuePrioritySerializer, BuiltInIssueSeveritySerializer, BuiltInIssueStatusSerializer, BuiltInIssueTypeSerializer, ComponentSerializer, ComponentDataSerializer, CustomIssuePrioritySerializer, CustomIssuePriorityDataSerializer, CustomIssueSeveritySerializer, CustomIssueSeverityDataSerializer, CustomIssueStatusSerializer, CustomIssueStatusDataSerializer, CustomIssueTypeSerializer, CustomIssueTypeDataSerializer, GitRepositorySerializer, GitRepositoryDataSerializer, IssueSerializer, IssueDataSerializer, ProjectSerializer, ProjectDataSerializer, VersionSerializer, VersionDataSerializer

from core.models import user as core_user_models
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.issue_type import BuiltInIssueType, CustomIssueType, CustomIssueTypeData
from project.models.issue import Issue, IssueData
from project.models.priority import BuiltInIssuePriority, CustomIssuePriority, CustomIssuePriorityData
from project.models.project import Project, ProjectData
from project.models.status import BuiltInIssueStatus, CustomIssueStatus, CustomIssueStatusData
from project.models.component import Component, ComponentData
from project.models.severity import BuiltInIssueSeverity, CustomIssueSeverity, CustomIssueSeverityData
from project.models.version import Version, VersionData


class BuiltInIssuePriorityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows built-in issue priorities to be viewed or edited.
    """

    queryset = BuiltInIssuePriority.active_objects.all()
    serializer_class = BuiltInIssuePrioritySerializer
    permission_classes = [permissions.IsAuthenticated]


class BuiltInIssueSeverityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows built-in issue priorities to be viewed or edited.
    """

    queryset = BuiltInIssueSeverity.active_objects.all()
    serializer_class = BuiltInIssueSeveritySerializer
    permission_classes = [permissions.IsAuthenticated]


class BuiltInIssueStatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows built-in issue statuses to be viewed or edited.
    """

    queryset = BuiltInIssueStatus.active_objects.all()
    serializer_class = BuiltInIssueStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class BuiltInIssueTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows built-in issue types to be viewed or edited.
    """

    queryset = BuiltInIssueType.active_objects.all()
    serializer_class = BuiltInIssueTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ComponentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue priorities to be viewed or edited.
    """

    queryset = Component.active_objects.all()
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAuthenticated]


class ComponentDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows built-in issue types to be viewed or edited.
    """

    queryset = ComponentData.active_objects.all()
    serializer_class = ComponentDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssuePriorityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue priorities to be viewed or edited.
    """

    queryset = CustomIssuePriority.active_objects.all()
    serializer_class = CustomIssuePrioritySerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssuePriorityDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue priorities to be viewed or edited.
    """

    queryset = CustomIssuePriorityData.active_objects.all()
    serializer_class = CustomIssuePriorityDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssueSeverityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue priorities to be viewed or edited.
    """

    queryset = CustomIssueSeverity.active_objects.all()
    serializer_class = CustomIssueSeveritySerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssueSeverityDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue priorities to be viewed or edited.
    """

    queryset = CustomIssueSeverityData.active_objects.all()
    serializer_class = CustomIssueSeverityDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssueStatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue statuses to be viewed or edited.
    """

    queryset = CustomIssueStatus.active_objects.all()
    serializer_class = CustomIssueStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssueStatusDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue statuses to be viewed or edited.
    """

    queryset = CustomIssueStatusData.active_objects.all()
    serializer_class = CustomIssueStatusDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssueTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue types to be viewed or edited.
    """

    queryset = CustomIssueType.active_objects.all()
    serializer_class = CustomIssueTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssueTypeDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue types to be viewed or edited.
    """

    queryset = CustomIssueTypeData.active_objects.all()
    serializer_class = CustomIssueTypeDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class GitRepositoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows git repositories to be viewed or edited.
    """

    queryset = GitRepository.active_objects.all()
    serializer_class = GitRepositorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=self.request.user)
        # Get unique repositories from organizations and projects
        organization_repositories = logged_in_user.organizationmembers_set.values_list('git_repositories', flat=True)
        project_repositories = logged_in_user.list_projects().values_list('git_repositories', flat=True)
        # Combine the repository IDs and get distinct repositories
        repository_ids = set(organization_repositories).union(set(project_repositories))
        repositories = GitRepository.objects.filter(id__in=repository_ids)
        return repositories.all()


class GitRepositoryDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows git repositories to be viewed or edited.
    """

    queryset = GitRepositoryData.active_objects.all()
    serializer_class = GitRepositoryDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows issues to be viewed or edited.
    """

    queryset = Issue.active_objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]


class IssueDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows issues to be viewed or edited.
    """

    queryset = IssueData.active_objects.all()
    serializer_class = IssueDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    queryset = Project.active_objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=self.request.user)
        return logged_in_user.list_projects()


class ProjectDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    queryset = ProjectData.active_objects.all()
    serializer_class = ProjectDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class VersionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows versions to be viewed or edited.
    """

    queryset = Version.active_objects.all()
    serializer_class = VersionSerializer
    permission_classes = [permissions.IsAuthenticated]


class VersionDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows versions to be viewed or edited.
    """

    queryset = VersionData.active_objects.all()
    serializer_class = VersionDataSerializer
    permission_classes = [permissions.IsAuthenticated]
