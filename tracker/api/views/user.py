from rest_framework import permissions, viewsets

from api.serializers.user import CoreUserSerializer, CoreUserDataSerializer

from core.models import user as core_user_models


class UserDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = core_user_models.CoreUserData.active_objects.all()
    serializer_class = CoreUserDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class CoreUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = core_user_models.CoreUser.active_objects.all()
    serializer_class = CoreUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # TODO: Limit this list to only the users in the organizations the user is a member of
    def get_queryset(self):
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=self.request.user)
        # Get unique users from owned organizations and projects
        organization_users = logged_in_user.organizationmembers_set.values_list('members', flat=True)
        # breakpoint()
        project_users = logged_in_user.list_projects().values_list('current__users', flat=True)
        # Managing users of an organization is a different view
        # Combine the user IDs and get distinct users
        user_ids = set(organization_users).union(set(project_users))
        users = core_user_models.CoreUser.objects.filter(id__in=user_ids)
        return users.all()
