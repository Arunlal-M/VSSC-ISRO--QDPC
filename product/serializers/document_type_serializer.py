from rest_framework import serializers
from qdpc_core_models.models.document_type import DocumentType

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'

    def validate_name(self, value):
            """Validate that the DocumentType name is unique."""
            if DocumentType.objects.filter(name=value).exists():
                raise serializers.ValidationError("A DocumentType with this name already exists.")
            return value
        
    
    