from rest_framework import permissions, viewsets

from api.serializers.user import UserSerializer

from core.models.user import CoreUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CoreUser.active_objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
