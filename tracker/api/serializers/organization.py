from rest_framework import serializers

from core.models.organization import Organization, OrganizationData
from .core import DeletedModelDataSerializer
from .core_user import CoreUserSerializer
from .project import ProjectSerializer, GitRepositorySerializer


class OrganizationDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganizationData
        fields = ['id', 'created_by', 'first_name', 'last_name', 'email', 'secondary_email', 'home_phone', 'mobile_phone', 'work_phone', 'address_line_1', 'address_line_2', 'postal_code', 'city', 'state', 'timezone', 'deleted']

    deleted = DeletedModelDataSerializer()


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'created_by', 'created_on', 'organization_data', 'is_paid', 'renewal_date', 'number_users_allowed', 'members', 'projects', 'repositories', 'deleted']

    deleted = DeletedModelDataSerializer()
    organization_data = OrganizationDataSerializer()
    members = CoreUserSerializer(many=True)
    projects = ProjectSerializer(many=True)
    repositories = GitRepositorySerializer(many=True)
