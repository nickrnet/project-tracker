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
    # def get_queryset(self):
    #     logged_in_user = core_user_models.CoreUser.objects.get(user__username=self.request.user)
    #     return logged_in_user.organizationmembers_set.all()
