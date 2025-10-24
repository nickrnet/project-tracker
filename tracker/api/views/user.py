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

    def get_queryset(self):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=self.request.user)
        users = logged_in_user.list_users()
        return users.all()
