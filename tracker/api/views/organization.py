from rest_framework import permissions, viewsets

from api.serializers.organization import OrganizationSerializer

from core.models.organization import Organization


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organizations to be viewed or edited.
    """
    queryset = Organization.active_objects.all().order_by('organization_data__name')
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
