


from rest_framework import serializers
from qdpc_core_models.models.role import Role
from qdpc_core_models.models.center import Center
from qdpc_core_models.models.user import User
from rest_framework import serializers
from qdpc_core_models.models.division import Division
  # Adjust the import according to your project structure

class UserUpdateSerializer(serializers.ModelSerializer):
    centre = serializers.PrimaryKeyRelatedField(queryset=Center.objects.all(), many=True)
    divisions = serializers.PrimaryKeyRelatedField(queryset=Division.objects.all(), many=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)

    class Meta:
        model = User
        fields = [
            'username', 'desired_salutation', 'user_id', 'first_name', 
            'last_name', 'email', 'centre', 'divisions', 'phone_number', 
            'usertype', 'password', 'is_active', 'is_staff', 'is_approved', 
            'role', 'date_joined', 'role_id'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
        }

    def create(self, validated_data):
        centres = validated_data.pop('centre')
        divisions = validated_data.pop('divisions')
        roles = validated_data.pop('role')

        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
            instance.save()

        instance.centre.set(centres)
        instance.divisions.set(divisions)
        instance.role.set(roles)

        return instance

    def update(self, instance, validated_data):
        print("Enterd updated data sucesfully")
        centres = validated_data.pop('centre', None)
        divisions = validated_data.pop('divisions', None)
        roles = validated_data.pop('role', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        if centres is not None:
            instance.centre.set(centres)
        if divisions is not None:
            instance.divisions.set(divisions)
        if roles is not None:
            instance.role.set(roles)

        print(instance,"The istance i got here")

        return instance
