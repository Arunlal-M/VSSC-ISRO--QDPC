from rest_framework import serializers
from qdpc_core_models.models.division import Division



class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ('id', 'name')