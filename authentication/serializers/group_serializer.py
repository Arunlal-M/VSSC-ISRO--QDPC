from rest_framework import serializers
from qdpc_core_models.models.role import Role


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')