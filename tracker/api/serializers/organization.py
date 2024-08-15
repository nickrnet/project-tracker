from rest_framework import serializers

from core.models.organization import Organization, OrganizationData
from .core import DeletedModelDataSerializer
from .user import UserSerializer
from .project import ProjectSerializer, GitRepositorySerializer


class OrganizationDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganizationData
        fields = [
            'name',
            'description',
            'responsible_party_email',
            'responsible_party_phone',
            'address_line_1',
            'address_line_2',
            'postal_code',
            'city',
            'state',
            'country',
            'timezone',
            'deleted'
        ]

    deleted = DeletedModelDataSerializer()


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'created_by', 'created_on', 'current', 'deleted']

    deleted = DeletedModelDataSerializer()
    current = OrganizationDataSerializer()
