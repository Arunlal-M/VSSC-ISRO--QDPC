from rest_framework import serializers
from qdpc_core_models.models.center import Center
from qdpc_core_models.models.user_type import UserType
from authentication.serializers.usertype_serializer import UserTypeSerializer 






class CenterSerializer(serializers.ModelSerializer):
    user_type = UserTypeSerializer(read_only=True)  # This will include UserType details
    user_type_id = serializers.PrimaryKeyRelatedField(queryset=UserType.objects.all(), source='user_type', write_only=True)

    class Meta:
        model = Center
        fields = ['id', 'name', 'user_type', 'user_type_id']

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        center = Center.objects.create(user_type=user_type, **validated_data)
        return center