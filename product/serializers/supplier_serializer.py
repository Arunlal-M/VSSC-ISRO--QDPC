from rest_framework import serializers
from qdpc_core_models.models.supplier import Suppliers

class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ['id', 'name','email','address']

    def validate_name(self, value):
        """Validate that the supplier name is unique."""
        if Suppliers.objects.filter(name=value).exists():
            raise serializers.ValidationError("A supplier with this name already exists.")
        return value
        
    def validate_email(self, value):
        """Validate that the supplier email is unique."""
        if Suppliers.objects.filter(email=value).exists():
            raise serializers.ValidationError("A supplier with this email already exists.")
        return value

    def validate_address(self, value):
        """Validate that the supplier address is unique."""
        if Suppliers.objects.filter(address=value).exists():
            raise serializers.ValidationError("A supplier with this address already exists.")
        return value