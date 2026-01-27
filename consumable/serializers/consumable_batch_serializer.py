from rest_framework import serializers
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.unit import Unit

class ConsumableBatchSerializer(serializers.ModelSerializer):
    consumable = serializers.PrimaryKeyRelatedField(queryset=Consumable.objects.all())
    batch_size_unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    consumable_name = serializers.SerializerMethodField()
    # calculate_expiry_date = serializers.SerializerMethodField()
    unit_name = serializers.SerializerMethodField()


    class Meta:
        model = ConsumableBatch
        fields = [
            'id',
            'consumable', 
            'consumable_name',
            'batch_id', 
            'procurement_date',
            'batch_size_value', 
            'batch_size_unit', 
            'packing_details',
            'status',
            'expiry_date',
            'unit_name'
        ]

    def get_consumable_name(self, obj):
        return obj.consumable.name

    # def get_calculate_expiry_date(self, obj):
    #     return obj.calculate_expiry_date  # Use the calculate_expiry_date method if it exists

    def get_unit_name(self, obj):
        return obj.batch_size_unit.abbreviation
    
    def create(self, validated_data):
        # Add additional logic here if needed
        return ConsumableBatch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        consumable = validated_data.pop('consumable', None)
        batch_size_unit = validated_data.pop('batch_size_unit', None)

        if consumable:
            instance.consumable = consumable
        if batch_size_unit:
            instance.batch_size_unit = batch_size_unit

        instance.batch_id = validated_data.get('batch_id', instance.batch_id)
        instance.procurement_date = validated_data.get('procurement_date', instance.procurement_date)
        instance.batch_size_value = validated_data.get('batch_size_value', instance.batch_size_value)
        instance.packing_details = validated_data.get('packing_details', instance.packing_details)
        instance.status = validated_data.get('status', instance.status)  # Ensure status is updated
        # Recalculate expiry date based on the updated data
     
        instance.save()
        return instance


   # consumable/serializers/combined_serializer.py

from qdpc_core_models.models.consumable_acceptance_test import ConsumableAcceptanceTest

class ConsumableBatchDetailedSerializer(serializers.ModelSerializer):
    acceptance_tests = serializers.SerializerMethodField()

    class Meta:
        model = ConsumableBatch
        fields = [
            'consumable',
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
        acceptance_tests = ConsumableAcceptanceTest.objects.filter(batch_id=obj.batch_id)
        return [
            {
                'batch_id' : test.batch_id,
                'consumable' : test.consumable.name,
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
