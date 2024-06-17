from django.contrib.auth.models import User
from rest_framework import serializers

from core.models.core import DeletedModel
from core.models.user import CoreUser, CoreUserData
from project.models.git_repository import GitRepository
from project.models.project import Project


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
    class Meta:
        model = CoreUser
        fields = ['id', 'created_by', 'core_user_data', 'user', 'deleted']

    core_user_data = CoreUserDataSerializer()
    user = UserSerializer()
    deleted = DeletedModelDataSerializer()


class GitRepositorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GitRepository
        fields = ['id', 'created_by', 'name', 'description', 'url', 'deleted']

    deleted = DeletedModelDataSerializer()


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'created_by', 'name', 'description', 'start_date', 'end_date', 'is_active', 'is_private', 'git_repository', 'users', 'deleted']

    deleted = DeletedModelDataSerializer()
