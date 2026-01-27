from rest_framework import serializers
from qdpc_core_models.models.process import Process, ProcessStep
from qdpc_core_models.models.product import Product
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.componentbatch import ComponentBatch
from qdpc_core_models.models.equipment import Equipment
from qdpc_core_models.models.unit import Unit
from datetime import date  # Add this import at the top

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'

class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = '__all__'

    def get_raw_materials(self, obj):
    # products = Product.objects.filter(process__name=obj.process)
    # raw_materials = []
    # for product in products:
    #     raw_materials.extend(product.raw_materials.values_list('name', flat=True))
        return 1

class ProcessNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'process'] 






# class ProcessSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Process
#         fields = ['process_title']

class RawMaterialBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialBatch
        fields = ['id', 'batch_id']  # Adjust fields as needed

class ConsumableBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumableBatch
        fields = ['id', 'batch_id']  # Adjust fields as needed

class ComponentBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentBatch
        fields = ['id', 'batch_id']  # Adjust fields as needed

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name']  # Adjust fields as needed

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']  # Adjust fields as needed


        

class ProcessStepSerializer(serializers.ModelSerializer):
    process = ProcessSerializer(read_only=True)
    raw_material_batch = RawMaterialBatchSerializer(many=True, read_only=True)
    consumable_batch = ConsumableBatchSerializer(many=True, read_only=True)
    component_batch = ComponentBatchSerializer(many=True, read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)
    unit = UnitSerializer(many=True, read_only=True)
    rawmaterial = serializers.SerializerMethodField()
    consumable = serializers.SerializerMethodField()
    component = serializers.SerializerMethodField()
    unit_options =serializers.SerializerMethodField()
    
   
    

    class Meta:
        model = ProcessStep
        fields = [
            'id',
            'process',
            'step_id',
            'raw_material_batch',
            'consumable_batch',
            'component_batch',
            'equipment',
            'process_description',
            'process_date',
            'rawmaterial',
            'min_value',
            'max_value',
            'unit',
            'test_result',
            'specification_result',
            'process_type',
            'rm_status',
            'equipment_status',
            'consumable_status',
            'component_status',
            'remarks',
            'consumable',
            'component',
            'unit_options'
            # Writable fields
            # 'raw_material_batch_ids',
            # 'consumable_batch_ids',
            # 'component_batch_ids',
            # 'equipment_ids',
            # 'unit_ids'
        ]
        read_only_fields = ['step_id']  # Since it's auto-generated in save()

    def get_rawmaterial(self, obj):
        # Get all products that have this process
        products = Product.objects.filter(process=obj.process)
        today = date.today() 
        
        # Collect all raw materials from these products
        raw_materials = []
        for product in products:
            for rm in product.rawmaterial.all():
                expiry_date = rm.calculate_expiry_date
                status = None
                if expiry_date:
                    status = "expired" if today > expiry_date else "valid"
                raw_materials.append({
                    'id': rm.id,
                    'name': rm.name,
                    'status':status,
                    'expiry_date': expiry_date.strftime('%Y-%m-%d') if expiry_date else None,
                     'suppliers': [{
                    'id': supplier.id,
                    'name': supplier.name
                } for supplier in rm.suppliers.all()]  ,#
                     
                'sources': [{
                    'id': source.id,
                    'name': source.name
                } for source in rm.sources.all()]  #

                }),

        # Remove duplicates (in case same raw material is used in multiple products)
        unique_raw_materials = []
        seen_ids = set()
        for rm in raw_materials:
            if rm['id'] not in seen_ids:
                seen_ids.add(rm['id'])
                unique_raw_materials.append(rm)
        
        return unique_raw_materials


    def get_consumable(self, obj):
    # Get all products that have this process
        products = Product.objects.filter(process=obj.process)
        today = date.today() 
        # Collect all consumables from these products
        consumables = []
        for product in products:
            for c in product.consumable.all():
                expiry_date = c.calculate_expiry_date
                status = None
                if expiry_date:
                    status = "expired" if today > expiry_date else "valid"
                consumables.append({
                    'id': c.id,
                    'name': c.name,
                    'status':status,
                    'suppliers': [{
                    'id': supplier.id,
                    'name': supplier.name
                } for supplier in c.suppliers.all()]  ,#
                     
                'sources': [{
                    'id': source.id,
                    'name': source.name
                } for source in c.sources.all()]  #
                    
                })
        
        # Remove duplicates
        unique_consumables = []
        seen_ids = set()
        for c in consumables:
            if c['id'] not in seen_ids:
                seen_ids.add(c['id'])
                unique_consumables.append(c)
        
        return unique_consumables




    def get_component(self, obj):
        # Get all products that have this process
        products = Product.objects.filter(process=obj.process)
        today = date.today() 
        
        # Collect all components from these products
        components = []
        for product in products:
            for comp in product.components.all():
                expiry_date = comp.calculate_expiry_date
               
                status = None
                if expiry_date:
                    status = "expired" if today > expiry_date else "valid"

                components.append({
                    'id': comp.id,
                    'name': comp.name,
                    'status':status,
                    'suppliers': [{
                    'id': supplier.id,
                    'name': supplier.name
                } for supplier in comp.suppliers.all()]  ,#
                     
                'sources': [{
                    'id': source.id,
                    'name': source.name
                } for source in comp.sources.all()]  #
                })
        # Remove duplicates
        unique_components = []
        seen_ids = set()
        for comp in components:
            if comp['id'] not in seen_ids:
                seen_ids.add(comp['id'])
                unique_components.append(comp)
        
        return unique_components


    def get_unit_options(self, obj):
        products = Product.objects.filter(process=obj.process)
        unit_options = []
        
        for product in products:
            for comp in product.components.all():
                for test in comp.component_acceptance_tests.all():
                    option = {
                    'unit_id': test.component_unit,
                    'batch_id': test.batch_id,
                    'source_id': test.sources.id,
                    'supplier_id': test.suppliers.id
                    }
                    unit_options.append(option)
        
        return unit_options




    def validate(self, data):
        """
        Custom validation for the process step
        """
        if data.get('min_value') is not None and data.get('max_value') is not None:
            if data['min_value'] > data['max_value']:
                raise serializers.ValidationError("Min value cannot be greater than max value")
        
        if data.get('process_type') == 'quantitative' and (data.get('min_value') is None or data.get('max_value') is None):
            raise serializers.ValidationError("Quantitative processes require both min and max values")
            
        return data

    def create(self, validated_data):
        """
        Custom create method to handle many-to-many relationships
        """
        # Pop the many-to-many fields
        raw_material_batches = validated_data.pop('raw_material_batch', [])
        consumable_batches = validated_data.pop('consumable_batch', [])
        component_batches = validated_data.pop('component_batch', [])
        equipments = validated_data.pop('equipment', [])
        units = validated_data.pop('unit', [])
        
        # Create the process step
        process_step = ProcessStep.objects.create(**validated_data)
        
        # Set the many-to-many relationships
        process_step.raw_material_batch.set(raw_material_batches)
        process_step.consumable_batch.set(consumable_batches)
        process_step.component_batch.set(component_batches)
        process_step.equipment.set(equipments)
        process_step.unit.set(units)
        
        return process_step

    def update(self, instance, validated_data):
        """
        Custom update method to handle many-to-many relationships
        """
        # Pop the many-to-many fields
        raw_material_batches = validated_data.pop('raw_material_batch', None)
        consumable_batches = validated_data.pop('consumable_batch', None)
        component_batches = validated_data.pop('component_batch', None)
        equipments = validated_data.pop('equipment', None)
        units = validated_data.pop('unit', None)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        # Update many-to-many relationships if they were provided
        if raw_material_batches is not None:
            instance.raw_material_batch.set(raw_material_batches)
        if consumable_batches is not None:
            instance.consumable_batch.set(consumable_batches)
        if component_batches is not None:
            instance.component_batch.set(component_batches)
        if equipments is not None:
            instance.equipment.set(equipments)
        if units is not None:
            instance.unit.set(units)
        
        return instance