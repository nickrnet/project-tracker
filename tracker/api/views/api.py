from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from api.serializers.serializers import CoreUserSerializer, UserSerializer

from core.models.user import CoreUser


class CoreUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CoreUser.active_objects.all().order_by('core_user_data__last_name')
    serializer_class = CoreUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
