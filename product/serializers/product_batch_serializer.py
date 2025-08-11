from rest_framework import serializers
from qdpc_core_models.models.product_batchlist import ProductBatch
from qdpc_core_models.models.product import Product
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.componentbatch import ComponentBatch
from qdpc_core_models.models.process import Process
from qdpc_core_models.models.unit import Unit
from qdpc_core_models.models.user import User

from qdpc_core_models.models.product import Product

# class ProductBatchDetailedSerializer(serializers.ModelSerializer):
#     """Serializer for product batch information."""
    
#     # Define fields for Many-to-Many relationships
#     product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
#     RawMaterial = serializers.PrimaryKeyRelatedField(queryset=RawMaterialBatch.objects.all())
#     consumable = serializers.PrimaryKeyRelatedField(queryset=ConsumableBatch.objects.all())
#     Component = serializers.PrimaryKeyRelatedField(queryset=ComponentBatch.objects.all())
#     Process = serializers.PrimaryKeyRelatedField(queryset=Process.objects.all())
#     batch_size_unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
#     created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
#     # SerializerMethodFields to provide readable names
#     product_name = serializers.SerializerMethodField()
#     unit_name = serializers.SerializerMethodField()
    
#     class Meta:
#         model = ProductBatch
#         fields = [
#             'product',
#             'product_name',
#             'unit_name',
#             'batch_id',
#             'RawMaterial',
#             'consumable',
#             'Component',
#             'Process',
#             'batch_size_value',
#             'batch_size_unit',
#             'manufacturings_start_date',
#             'manufacturings_end_date',
#             'packing_details',
#             'created_by'
#         ]
        
#     def get_product_name(self, obj):
#         return obj.product.name
    
#     def get_unit_name(self, obj):
#         return obj.batch_size_unit.abbreviation





# from rest_framework import serializers
# from qdpc_core_models.models.product_batchlist import ProductBatch

# from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
# from qdpc_core_models.models.consumablebatch import ConsumableBatch
# from qdpc_core_models.models.componentbatch import ComponentBatch
# from qdpc_core_models.models.process import Process
# from qdpc_core_models.models.unit import Unit
# from qdpc_core_models.models.user import User

# class ProductBatchDetailedSerializer(serializers.ModelSerializer):
#     """Serializer for product batch information."""
    
#     # Make these fields optional since they might come from the request
#     raw_material_batch = serializers.PrimaryKeyRelatedField(
#         queryset=RawMaterialBatch.objects.all(),
#         required=False
#     )
#     consumable_batch = serializers.PrimaryKeyRelatedField(
#         queryset=ConsumableBatch.objects.all(),
#         required=False
#     )
#     component_batch = serializers.PrimaryKeyRelatedField(
#         queryset=ComponentBatch.objects.all(),
#         required=False
#     )
#     process = serializers.PrimaryKeyRelatedField(
#         queryset=Process.objects.all(),
#         required=False
#     )
#     created_by = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#         required=False
#     )
    
#     class Meta:
#         model = ProductBatch
#         fields = [
#             'batch_id',
#             'product',
#             'raw_material_batch',
#             'consumable_batch',
#             'component_batch',
#             'process',
#             'batch_size_value',
#             'batch_size_unit',
#             'manufacturings_start_date',
#             'manufacturings_end_date',
#             'packing_details',
#             'status',
#             'created_by',
#             'qa_approval_date',
#             'qa_approved_by',
#             'rejection_reason'
#         ]
#         extra_kwargs = {
#             'batch_id': {'required': True},
#             'product': {'required': True},
#             'batch_size_value': {'required': True},
#             'batch_size_unit': {'required': True},
#             'manufacturings_start_date': {'required': True},
#             'manufacturings_end_date': {'required': True},
#             'packing_details': {'required': True},
#         }

#     def validate(self, data):
#         """Custom validation for the serializer"""
#         # Ensure required fields are present
#         required_fields = [
#             'batch_id', 'product', 'batch_size_value', 
#             'batch_size_unit', 'manufacturings_start_date',
#             'manufacturings_end_date', 'packing_details'
#         ]
        
#         for field in required_fields:
#             if field not in data:
#                 raise serializers.ValidationError({field: "This field is required."})
        
#         return data





# from rest_framework import serializers
# from qdpc_core_models.models.product_batchlist import ProductBatch
# from qdpc_core_models.models.product import Product
# from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
# from qdpc_core_models.models.consumablebatch import ConsumableBatch
# from qdpc_core_models.models.componentbatch import ComponentBatch
# from qdpc_core_models.models.process import Process
# from qdpc_core_models.models.unit import Unit
# from qdpc_core_models.models.user import User

# class ProductBatchDetailedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductBatch
#         fields = [
#             'batch_id',
#             'product',
#             'raw_material_batch',
#             'consumable_batch',
#             'component_batch',
#             'Process',
#             'batch_size_value',
#             'batch_size_unit',
#             'manufacturings_start_date',
#             'manufacturings_end_date',
#             'packing_details',
#             'status',
           
           
#         ]
      
#     def create(self, validated_data):
#         # Set created_by from context if available
#         user = self.context['request'].user if 'request' in self.context else None
#         if user and user.is_authenticated:
#             validated_data['created_by'] = user
#         return super().create(validated_data)


# class ProductBatchDetailedSerializer(serializers.ModelSerializer):

#     product_name = serializers.SerializerMethodField()
    
#     class Meta:
#         model = ProductBatch
#         fields = [
#             'id',
#             'batch_id',
#             'product',
#             'product_name',
#             'raw_material_batch',
#             'consumable_batch',
#             'component_batch',
#             'Process',
#             'batch_size_value',
#             'batch_size_unit',
#             'manufacturings_start_date',
#             'manufacturings_end_date',
#             'packing_details',
#             'status',
#             'created_on',
#             'created_by',
#             'qa_approval_date',
#             'qa_approved_by',
#             'rejection_reason',
#         ]
#         read_only_fields = ['created_on', 'qa_approval_date', 'qa_approved_by']

#     def get_product_name(self, obj):
#         return obj.product.name if obj.product else None

#     def create(self, validated_data):
#         # Set created_by from context if available
#         user = self.context['request'].user if 'request' in self.context else None
#         if user and user.is_authenticated:
#             validated_data['created_by'] = user
#         return super().create(validated_data)



class ProductBatchDetailedSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    dynamic_tables_data = serializers.JSONField(required=False, allow_null=True)  # Add this line
    
    class Meta:
        model = ProductBatch
        fields = [
            'id',
            'batch_id',
            'product',
            'product_name',
            'raw_material_batch',
            'consumable_batch',
            'component_batch',
            'Process',
            'batch_size_value',
            'batch_size_unit',
            'manufacturings_start_date',
            'manufacturings_end_date',
            'packing_details',
            'status',
            'created_on',
            'created_by',
            'qa_approval_date',
            'qa_approved_by',
            'rejection_reason',
            'dynamic_tables_data',  # Add this field
        ]
        read_only_fields = ['created_on', 'qa_approval_date', 'qa_approved_by']

    def get_product_name(self, obj):
        return obj.product.name if obj.product else None

    def create(self, validated_data):
        # Set created_by from context if available
        user = self.context['request'].user if 'request' in self.context else None
        if user and user.is_authenticated:
            validated_data['created_by'] = user
        
        # Handle dynamic_tables_data if present in the request
        dynamic_tables = validated_data.pop('dynamic_tables_data', None)
        instance = super().create(validated_data)
        
        if dynamic_tables is not None:
            instance.dynamic_tables_data = dynamic_tables
            instance.save()
        
        return instance

    def update(self, instance, validated_data):
        # Handle dynamic_tables_data updates
        dynamic_tables = validated_data.pop('dynamic_tables_data', None)
        instance = super().update(instance, validated_data)
        
        if dynamic_tables is not None:
            instance.dynamic_tables_data = dynamic_tables
            instance.save()
        
        return instance