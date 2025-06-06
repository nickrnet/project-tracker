from rest_framework import serializers

from core.models.organization import Organization, OrganizationData
from .core import DeletedModelDataSerializer
from .user import CoreUserSerializer
from .project import GitRepositorySerializer
from .project import ProjectSerializer


class OrganizationDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrganizationData
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
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
            'is_paid',
            'renewal_date',
            'number_users_allowed',
            ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current',
            'members',
            'git_repositories',
            'projects',
            ]

    created_by = CoreUserSerializer()
    deleted = DeletedModelDataSerializer()
    current = OrganizationDataSerializer()
    members = CoreUserSerializer(many=True)
    git_repositories = GitRepositorySerializer(many=True)
    projects = ProjectSerializer(many=True)
