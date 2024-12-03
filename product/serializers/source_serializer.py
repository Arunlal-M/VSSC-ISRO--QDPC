from rest_framework import serializers
from qdpc_core_models.models.source import Sources

class SourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sources
        fields = ['id', 'name','email','address']
