from rest_framework import serializers

from django.contrib.auth.models import User as DjangoUser

from core.models import user as core_user_models
from .core import DeletedModelDataSerializer


class DjangoUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ['username', 'email',]


class CoreUserDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = core_user_models.CoreUserData
        fields = ['id', 'created_by', 'first_name', 'last_name', 'email', 'secondary_email', 'home_phone', 'mobile_phone', 'work_phone', 'address_line_1', 'address_line_2', 'postal_code', 'city', 'state', 'timezone',]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = core_user_models.CoreUser
        fields = ['id', 'created_by', 'current', 'user', 'deleted']

    current = CoreUserDataSerializer()
    user = DjangoUserSerializer()
    deleted = DeletedModelDataSerializer()
