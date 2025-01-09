from rest_framework import serializers
from qdpc_core_models.models.document_type import DocumentType

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'
