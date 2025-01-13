from rest_framework import serializers
from qdpc_core_models.models.unit import Unit

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

    def validate_name(self, value):
        """Validate that the Unit name is unique."""
        if Unit.objects.filter(name=value).exists():
            raise serializers.ValidationError("A Unit with this name already exists.")
        return value
        
    def validate_abbreviation(self, value):
        """Validate that the Unit email is unique."""
        if Unit.objects.filter(abbreviation=value).exists():
            raise serializers.ValidationError("A Unit with this abbreviation already exists.")
        return value

    