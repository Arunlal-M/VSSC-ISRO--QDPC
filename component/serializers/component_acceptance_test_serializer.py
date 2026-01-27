from rest_framework import serializers
from qdpc_core_models.models.component_acceptance_test import ComponentAcceptanceTest
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.grade import Grade

class AcceptanceTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentAcceptanceTest
        fields = [
            'id',
            'test_value',
            'min_value',
            'max_value',
            'file',
            'status',
            'remark',
            'created_by'
        ]
    # Ensure the file field is optional to handle cases without file uploads
    file = serializers.FileField(required=False)

class ComponentAcceptanceTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentAcceptanceTest
        fields = [
            'batch_id',
            'component',
            'component_unit',   # <-- Add this line
            'sources',
            'suppliers',
            'grade',
            'test_value',
            'min_value',
            'max_value',
            'file',
            'status',
            'remark',
            'created_by',
            'acceptance_test'
        ]
        
    # Set related fields to PrimaryKeyRelatedField to accept IDs
    component = serializers.PrimaryKeyRelatedField(queryset=Component.objects.all())
    acceptance_test = serializers.PrimaryKeyRelatedField(queryset=AcceptanceTest.objects.all())
    sources = serializers.PrimaryKeyRelatedField(queryset=Sources.objects.all())
    suppliers = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all())
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), required=False, allow_null=True)  # Nullable grade

    def create(self, validated_data):
        return ComponentAcceptanceTest.objects.create(**validated_data)
