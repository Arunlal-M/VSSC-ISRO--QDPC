from rest_framework import serializers
from qdpc_core_models.models.componentbatch import ComponentBatch
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.unit import Unit

class ComponentBatchSerializer(serializers.ModelSerializer):
    component = serializers.PrimaryKeyRelatedField(queryset=Component.objects.all())
    batch_size_unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    component_name = serializers.SerializerMethodField()
    # calculate_expiry_date = serializers.SerializerMethodField()
    unit_name = serializers.SerializerMethodField()


    class Meta:
        model = ComponentBatch
        fields = [
            'id',
            'component', 
            'component_name',
            'batch_id', 
            'procurement_date',
            'batch_size_value', 
            'batch_size_unit', 
            'packing_details',
            'status',
            'expiry_date',
            'unit_name'
        ]

    def get_component_name(self, obj):
        return obj.component.name

    # def get_calculate_expiry_date(self, obj):
    #     return obj.calculate_expiry_date  # Use the calculate_expiry_date method if it exists

    def get_unit_name(self, obj):
        return obj.batch_size_unit.abbreviation
    
    def create(self, validated_data):
        # Add additional logic here if needed
        return ComponentBatch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        component = validated_data.pop('component', None)
        batch_size_unit = validated_data.pop('batch_size_unit', None)

        if component:
            instance.component = component
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
