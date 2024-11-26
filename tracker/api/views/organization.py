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
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=self.request.user)
        return logged_in_user.organizationmembers_set.all()


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organizations to be viewed or edited.
    """

    queryset = Organization.active_objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        orgs_to_return = []
        logged_in_user = core_user_models.CoreUser.objects.get(user__username=self.request.user)
        for org_data in logged_in_user.organizationmembers_set.all():
            if org_data.organization.id not in orgs_to_return:
                orgs_to_return.append(org_data.organization.id)

        return Organization.objects.filter(id__in=orgs_to_return).all()
