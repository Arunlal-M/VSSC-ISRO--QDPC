from rest_framework import serializers
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.unit import Unit

class RawMaterialBatchSerializer(serializers.ModelSerializer):
    raw_material = serializers.PrimaryKeyRelatedField(queryset=RawMaterial.objects.all())
    batch_size_unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    raw_material_name = serializers.SerializerMethodField()
    unit_name = serializers.SerializerMethodField()

    class Meta:
        model = RawMaterialBatch
        fields = [
            'id',
            'raw_material', 
            'raw_material_name',
            'batch_id', 
            'procurement_date',
            'batch_size_value', 
            'batch_size_unit', 
            'packing_details',
            'status',
            'expiry_date',
            'unit_name'
        ]
        read_only_fields = ['id', 'created_on', 'created_by']

    def get_raw_material_name(self, obj):
        return obj.raw_material.name if obj.raw_material else None

    def get_unit_name(self, obj):
        return obj.batch_size_unit.abbreviation if obj.batch_size_unit else None
    
    def validate_batch_id(self, value):
        # Check if batch_id already exists (for create operations)
        if self.instance is None:  # This is a create operation
            if RawMaterialBatch.objects.filter(batch_id=value).exists():
                raise serializers.ValidationError("A batch with this ID already exists.")
        return value
    
    def validate_batch_size_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Batch size value must be greater than zero.")
        return value
    
    def validate_procurement_date(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Procurement date cannot be in the future.")
        return value
    
    def validate_expiry_date(self, value):
        if value:
            procurement_date = self.initial_data.get('procurement_date')
            if procurement_date:
                # Convert procurement_date to date object if it's a string
                if isinstance(procurement_date, str):
                    from datetime import datetime
                    try:
                        procurement_date = datetime.strptime(procurement_date, '%Y-%m-%d').date()
                    except ValueError:
                        raise serializers.ValidationError("Invalid procurement date format.")
                
                if value <= procurement_date:
                    raise serializers.ValidationError("Expiry date must be after procurement date.")
        return value
    
    def validate(self, data):
        """Custom validation for the entire data set"""
        # Validate that if raw material has shelf life, expiry date should be calculated
        raw_material = data.get('raw_material')
        if raw_material and raw_material.shelf_life_value and raw_material.shelf_life_unit:
            if not data.get('expiry_date'):
                raise serializers.ValidationError("Expiry date is required for materials with shelf life.")
        
        return data

    def create(self, validated_data):
        # Add default status if not provided
        if 'status' not in validated_data:
            validated_data['status'] = 'available'
        
        batch = RawMaterialBatch.objects.create(**validated_data)
        return batch

    def update(self, instance, validated_data):
        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
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
