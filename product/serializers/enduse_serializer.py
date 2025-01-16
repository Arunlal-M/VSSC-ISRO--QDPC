from rest_framework import serializers
from qdpc_core_models.models.enduse import EndUse

class EnduseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUse
        fields = '__all__'

    def validate_name(self, value):
            """Validate that the EndUse name is unique."""
            if EndUse.objects.filter(name=value).exists():
                raise serializers.ValidationError("A EndUse with this name already exists.")
            return value
        
    