from rest_framework import serializers
from qdpc_core_models.models.unit import Unit

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
