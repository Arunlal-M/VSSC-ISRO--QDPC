from rest_framework import serializers
from qdpc_core_models.models.grade import Grade

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

    def validate_name(self, value):
        """Validate that the Grade name is unique."""
        if Grade.objects.filter(name=value).exists():
            raise serializers.ValidationError("A Grade with this name already exists.")
        return value
        
    def validate_abbreviation(self, value):
        """Validate that the Unit email is unique."""
        if Grade.objects.filter(abbreviation=value).exists():
            raise serializers.ValidationError("A Grade with this abbreviation already exists.")
        return value
