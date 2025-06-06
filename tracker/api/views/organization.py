from rest_framework import permissions, viewsets

from api.serializers.organization import OrganizationSerializer, OrganizationDataSerializer

from core.models.organization import Organization, OrganizationData
from core.models import user as core_user_models


class OrganizationDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organizations to be viewed or edited.
    """

    queryset = OrganizationData.active_objects.all()
    serializer_class = OrganizationDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=self.request.user)
        return OrganizationData.active_objects.filter(id__in=logged_in_user.list_organizations().values('current'))


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organizations to be viewed or edited.
    """

    queryset = Organization.active_objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logged_in_user = core_user_models.CoreUser.active_objects.get(user__username=self.request.user)

        return logged_in_user.list_organizations()
