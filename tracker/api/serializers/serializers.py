from django.contrib.auth.models import User
from rest_framework import serializers

from core.models.core import DeletedModel
from core.models.user import CoreUser, CoreUserData


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email',]


class DeletedModelDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeletedModel
        fields = ['id', 'deleted_on', 'deleted_by', 'soft_deleted', 'hard_deleted',]


class CoreUserDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CoreUserData
        fields = ['id', 'created_by', 'first_name', 'last_name', 'email', 'secondary_email', 'home_phone', 'mobile_phone', 'work_phone', 'address_line_1', 'address_line_2', 'postal_code', 'city', 'state', 'timezone',]


class CoreUserSerializer(serializers.HyperlinkedModelSerializer):
    core_user_data = CoreUserDataSerializer()
    user = UserSerializer()
    deleted = DeletedModelDataSerializer()

    class Meta:
        model = CoreUser
        fields = ['id', 'created_by', 'core_user_data', 'user', 'deleted']
