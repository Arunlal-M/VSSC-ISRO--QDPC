from rest_framework import serializers
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.unit import Unit

class RawMaterialBatchSerializer(serializers.ModelSerializer):
    raw_material = serializers.PrimaryKeyRelatedField(queryset=RawMaterial.objects.all())
    batch_size_unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    raw_material_name = serializers.SerializerMethodField()
    # calculate_expiry_date = serializers.SerializerMethodField()

    class Meta:
        model = RawMaterialBatch
        fields = [
            'raw_material', 
            'raw_material_name',
            'batch_id', 
            'procurement_date',
            'batch_size_value', 
            'batch_size_unit', 
            'packing_details'
        ]

    def get_raw_material_name(self, obj):
        return obj.raw_material.name

    # def get_calculate_expiry_date(self, obj):
    #     return obj.calculate_expiry_date  # Use the calculate_expiry_date method if it exists

   
    def create(self, validated_data):
        # Add additional logic here if needed
        return RawMaterialBatch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        raw_material = validated_data.pop('raw_material', None)
        batch_size_unit = validated_data.pop('batch_size_unit', None)

        if raw_material:
            instance.raw_material = raw_material
        if batch_size_unit:
            instance.batch_size_unit = batch_size_unit

        instance.batch_id = validated_data.get('batch_id', instance.batch_id)
        instance.procurement_date = validated_data.get('procurement_date', instance.procurement_date)
        instance.batch_size_value = validated_data.get('batch_size_value', instance.batch_size_value)
        instance.packing_details = validated_data.get('packing_details', instance.packing_details)

        # Recalculate expiry date based on the updated data
     
        instance.save()
        return instance
    
    
    
    # consumable/serializers/combined_serializer.py

from qdpc_core_models.models.raw_material_acceptence_test import RawMaterialAcceptanceTest

class RawMaterialBatchDetailedSerializer(serializers.ModelSerializer):
    acceptance_tests = serializers.SerializerMethodField()

    class Meta:
        model = RawMaterialBatch
        fields = [
            'raw_material',
            'batch_id',
            'procurement_date',
            'batch_size_value',
            'batch_size_unit',
            'packing_details',
            'created_on',
            'created_by',
            'acceptance_tests'
        ]

    def get_acceptance_tests(self, obj):
        acceptance_tests = RawMaterialAcceptanceTest.objects.filter(batch_id=obj.batch_id)
        return [
            {
                'batch_id' : test.batch_id,
                'raw_material' : test.raw_material.name,
                'acceptance_test': test.acceptance_test.name,
                'test_value': test.test_value,
                'sources': test.sources.name,
                'suppliers': test.suppliers.name,
                'grade': test.grade.name,
                'min_value': test.min_value,
                'max_value': test.max_value,
                'file': test.file.url if test.file else None,
                'status': test.status,
                'remark': test.remark,
                'created_by': test.created_by
            }
            for test in acceptance_tests
        ]
