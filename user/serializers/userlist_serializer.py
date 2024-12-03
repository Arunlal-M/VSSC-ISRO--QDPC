from rest_framework import serializers
from qdpc_core_models.models.user import User

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']






# class UpdateUserStatusSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     username = serializers.CharField(max_length=254)
#     is_active = serializers.BooleanField()
    

#     def update(self, instance, validated_data):
#         instance.is_active = validated_data.get('is_active', instance.is_active)
#         instance.save()
#         return instance

#     def validate(self, data):
#         try:
#             user = User.objects.get(id=data.get('id'), username=data.get('username'))
#         except User.DoesNotExist:
#             raise serializers.ValidationError("User not found.")
#         return data



class UpdateUserStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    is_active = serializers.BooleanField()

    def validate_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User with this ID does not exist.")
        return value
