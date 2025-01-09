from rest_framework import serializers
from qdpc_core_models.models.enduse import EndUse

class EnduseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUse
        fields = '__all__'
