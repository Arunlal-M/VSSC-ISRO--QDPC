from rest_framework import serializers
from qdpc_core_models.models.user_type import UserType



class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['id', 'name']