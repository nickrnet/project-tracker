from rest_framework import permissions, viewsets

from api.serializers.project import GitRepositorySerializer, GitRepositoryDataSerializer, BuiltInIssuePrioritySerializer, CustomIssuePrioritySerializer, BuiltInIssueStatusSerializer, CustomIssueStatusSerializer, BuiltInIssueTypeSerializer, CustomIssueTypeSerializer, IssueSerializer, ProjectDataSerializer, ProjectSerializer

from core.models import user as core_user_models
from project.models.git_repository import GitRepository, GitRepositoryData
from project.models.issue_type import BuiltInIssueType, CustomIssueType
from project.models.issue import Issue
from project.models.priority import BuiltInIssuePriority, CustomIssuePriority
from project.models.project import Project, ProjectData
from project.models.status import BuiltInIssueStatus, CustomIssueStatus


class BuiltInIssuePriorityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows built-in issue priorities to be viewed or edited.
    """
    queryset = BuiltInIssuePriority.active_objects.all()
    serializer_class = BuiltInIssuePrioritySerializer
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


class CustomIssuePriorityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue priorities to be viewed or edited.
    """
    queryset = CustomIssuePriority.active_objects.all()
    serializer_class = CustomIssuePrioritySerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssueStatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue statuses to be viewed or edited.
    """
    queryset = CustomIssueStatus.active_objects.all()
    serializer_class = CustomIssueStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomIssueTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows custom issue types to be viewed or edited.
    """
    queryset = CustomIssueType.active_objects.all()
    serializer_class = CustomIssueTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class GitRepositoryDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows git repositories to be viewed or edited.
    """
    queryset = GitRepositoryData.active_objects.all()
    serializer_class = GitRepositoryDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class GitRepositoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows git repositories to be viewed or edited.
    """
    queryset = GitRepository.active_objects.all()
    serializer_class = GitRepositorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=self.request.user)
        return logged_in_user.gitrepository_created_by.all()


class IssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows issues to be viewed or edited.
    """
    queryset = Issue.active_objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = ProjectData.active_objects.all()
    serializer_class = ProjectDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.active_objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=self.request.user)
        return logged_in_user.project_created_by.all()
