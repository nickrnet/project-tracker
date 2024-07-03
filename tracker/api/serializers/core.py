from rest_framework import serializers

from core.models.core import DeletedModel


class DeletedModelDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeletedModel
        fields = ['id', 'deleted_on', 'deleted_by', 'soft_deleted', 'hard_deleted',]
