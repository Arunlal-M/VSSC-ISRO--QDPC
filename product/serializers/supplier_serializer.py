from rest_framework import serializers
from qdpc_core_models.models.supplier import Suppliers

class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ['id', 'name','email','address']
