from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from api.serializers.serializers import CoreUserSerializer, GitRepositorySerializer, ProjectSerializer, UserSerializer

from core.models.user import CoreUser
from project.models.git_repository import GitRepository
from project.models.project import Project


class CoreUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CoreUser.active_objects.all().order_by('core_user_data__last_name')
    serializer_class = CoreUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GitRepositoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows git repositories to be viewed or edited.
    """
    queryset = GitRepository.active_objects.all().order_by('name')
    serializer_class = GitRepositorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    queryset = Project.active_objects.all().order_by('name')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
