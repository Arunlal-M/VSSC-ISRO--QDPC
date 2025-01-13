from rest_framework import serializers
from qdpc_core_models.models.source import Sources

class SourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sources
        fields = ['id', 'name','email','address']
        
    def validate_name(self, value):
        """Validate that the Source name is unique."""
        if Sources.objects.filter(name=value).exists():
            raise serializers.ValidationError("A Source with this name already exists.")
        return value
        
    def validate_email(self, value):
        """Validate that the Source email is unique."""
        if Sources.objects.filter(email=value).exists():
            raise serializers.ValidationError("A Source with this email already exists.")
        return value
    
    def validate_address(self, value):
        """Validate that the Source address is unique."""
        if Sources.objects.filter(address=value).exists():
            raise serializers.ValidationError("A Source with this address already exists.")
        return value

    