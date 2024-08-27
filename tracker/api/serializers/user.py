from rest_framework import serializers

from django.contrib.auth.models import User as DjangoUser

from core.models import user as core_user_models
from .core import DeletedModelDataSerializer


class DjangoUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DjangoUser
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}


class CoreUserDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = core_user_models.CoreUserData
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'first_name',
            'last_name',
            'email',
            'secondary_email',
            'home_phone',
            'mobile_phone',
            'work_phone',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'postal_code',
            'timezone',
        ]


class CoreUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = core_user_models.CoreUser
        fields = [
            'id',
            'created_by',
            'created_on',
            'deleted',
            'current',
            'user',
        ]

    # TODO: Get created_by to work with the CoreUserSerializer; it's nested so it's nasty
    current = CoreUserDataSerializer()
    user = DjangoUserSerializer()
    deleted = DeletedModelDataSerializer()
