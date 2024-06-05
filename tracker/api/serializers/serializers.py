from django.contrib.auth.models import Group, User
from rest_framework import serializers

from core.models.user import CoreUser, CoreUserData


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email',]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name',]


class CoreUserDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CoreUserData
        fields = ['created_by', 'id', 'first_name', 'last_name', 'email', 'secondary_email', 'home_phone', 'mobile_phone', 'work_phone', 'address_line_1', 'address_line_2', 'postal_code', 'city', 'state', 'timezone',]


class CoreUserSerializer(serializers.HyperlinkedModelSerializer):
    core_user_data = CoreUserDataSerializer()
    user = UserSerializer()

    class Meta:
        model = CoreUser
        fields = ['core_user_data', 'user',]
