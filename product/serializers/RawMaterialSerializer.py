from rest_framework import serializers
from qdpc_core_models.models.raw_material import RawMaterial
from product.serializers.source_serializer import SourcesSerializer
from product.serializers.supplier_serializer import SuppliersSerializer
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.grade import Grade
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from product.serializers.rawmaterial_batch_serializer import RawMaterialBatchSerializer  
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.componentbatch import ComponentBatch
from component.serializers.component_batch_serializer import ComponentBatchSerializer
from consumable.serializers.consumable_batch_serializer import ConsumableBatchSerializer
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.product import Drawing
from qdpc_core_models.models.acceptance_test_result import AcceptanceTestResult
from qdpc_core_models.models.rawmaterialGradeAcceptance import RawMaterialGradeAcceptanceTest
from qdpc_core_models.models.raw_material_acceptence_test import RawMaterialAcceptanceTest
from qdpc_core_models.models.equipment import *
from qdpc_core_models.models.process import Process
from qdpc_core_models.models.product_acceptence import ProductAcceptanceTest
from django.db import models
from qdpc_core_models.models import Product, Unit, RawMaterial, Component, Consumable, Equipment, AcceptanceTest


from qdpc_core_models.models.productBatch import *


class RawMaterialSerializer(serializers.ModelSerializer):
    # Define fields for Many-to-Many relationships
    sources = serializers.PrimaryKeyRelatedField(queryset=Sources.objects.all(), many=True)
    suppliers = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all(), many=True)
    acceptance_test = serializers.PrimaryKeyRelatedField(queryset=AcceptanceTest.objects.all(), many=True)
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), many=True)
    
    # SerializerMethodFields to provide readable names
    # calculate_expiry_date = serializers.SerializerMethodField()
    source_names = serializers.SerializerMethodField()
    supplier_names = serializers.SerializerMethodField()
    acceptance_test_names = serializers.SerializerMethodField()
    grade_names = serializers.SerializerMethodField()

    class Meta:
        model = RawMaterial
        fields = [
            'id',
            'name',
            'sources',
            'is_active',
            'suppliers',
            'grade',
            'shelf_life_type',  # New field for the shelf life type
            'shelf_life_value',
            'acceptance_test',
            'shelf_life_unit',
            # 'user_defined_date',
            'source_names',
            'supplier_names',
            'grade_names',
            # 'calculate_expiry_date',
            'acceptance_test_names',
        ]

    def validate_shelf_life_value(self, value):
        """Ensure shelf_life_value is numeric (float or integer)."""
        if value is not None and not isinstance(value, (float, int)):
            raise serializers.ValidationError("Shelf life value must be a numeric type.")
        return value

    # def get_calculate_expiry_date(self, obj):
    #     return obj.calculate_expiry_date

    def get_source_names(self, obj):
         return [source.name for source in obj.sources.all()]

    def get_supplier_names(self, obj):
        return [supplier.name for supplier in obj.suppliers.all()]
    
    def get_grade_names(self, obj):
        return [grade.name for grade in obj.grade.all()]

    def get_acceptance_test_names(self, obj):
        # Ensure obj.acceptance_tests.all() returns AcceptanceTest instances
        return [test.name for test in obj.acceptance_test.all()]

    def validate(self, data):
        # Ensure shelf_life_value and shelf_life_unit are None when shelf_life_type is 'not_applicable' or 'tbd'
        shelf_life_type = data.get('shelf_life_type')
        if shelf_life_type in ['not_applicable', 'tbd']:
            data['shelf_life_value'] = None
            data['shelf_life_unit'] = None
        return data

    def create(self, validated_data):
        sources = validated_data.pop('sources', [])
        suppliers = validated_data.pop('suppliers', [])
        grades = validated_data.pop('grade', [])
        acceptance_test = validated_data.pop('acceptance_test', [])

        raw_material = RawMaterial.objects.create(**validated_data)

        # Set many-to-many relationships
        raw_material.sources.set(sources)
        raw_material.suppliers.set(suppliers)
        raw_material.grade.set(grades)
        raw_material.acceptance_test.set(acceptance_test)

        return raw_material

    def update(self, instance, validated_data):
        sources = validated_data.pop('sources', None)
        suppliers = validated_data.pop('suppliers', None)
        grades = validated_data.pop('grade', None)
        acceptance_test = validated_data.pop('acceptance_test', None)

        instance.name = validated_data.get('name', instance.name)
        instance.shelf_life_value = validated_data.get('shelf_life_value', instance.shelf_life_value)
        instance.shelf_life_unit = validated_data.get('shelf_life_unit', instance.shelf_life_unit)
        instance.user_defined_date = validated_data.get('user_defined_date', instance.user_defined_date)
        instance.save()

        if sources is not None:
            instance.sources.set(sources)

        if suppliers is not None:
            instance.suppliers.set(suppliers)

        if grades is not None:
            instance.grade.set(grades)

        if acceptance_test is not None:
            instance.acceptance_test.set(acceptance_test)

        return instance
    


class RawMaterialWithBatchesSerializer(serializers.ModelSerializer):
    source_names = serializers.SerializerMethodField()
    supplier_names = serializers.SerializerMethodField()
    batches = serializers.SerializerMethodField()
  

    class Meta:
        model = RawMaterial
        fields = [
            'id',
            'name',
            'source_names',
            'supplier_names',
            'shelf_life_type',
            'shelf_life_value',
            'shelf_life_unit',
            'precertified',
            'batches',
              
        ]

    def get_source_names(self, obj):
        sources = obj.sources.all()
        return [sources[0].name] if sources.exists() else []

    def get_supplier_names(self, obj):
        return [s.name for s in obj.suppliers.all()]

    def get_batches(self, obj):
        batches = RawMaterialBatch.objects.filter(raw_material=obj)
        return RawMaterialBatchSerializer(batches, many=True).data



class ComponentWithBatchesSerializer(serializers.ModelSerializer):
    source_names = serializers.SerializerMethodField()
    supplier_names = serializers.SerializerMethodField()
    grade_names = serializers.SerializerMethodField()
    batches = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = [
            'id',
            'name',
            'source_names',
            'supplier_names',
            'grade_names',
            'shelf_life_type',
            'shelf_life_value',
            'shelf_life_unit',
            'batches',
        ]

    def get_source_names(self, obj):
        return [s.name for s in obj.sources.all()]

    def get_supplier_names(self, obj):
        return [s.name for s in obj.suppliers.all()]

    def get_grade_names(self, obj):
        return [g.name for g in obj.grade.all()]

    def get_batches(self, obj):
        batches = ComponentBatch.objects.filter(component=obj)
        return ComponentBatchSerializer(batches, many=True).data
class ConsumableWithBatchesSerializer(serializers.ModelSerializer):
    source_names = serializers.SerializerMethodField()
    supplier_names = serializers.SerializerMethodField()
    grade_names = serializers.SerializerMethodField()
    batches = serializers.SerializerMethodField()

    class Meta:
        model = Consumable
        fields = [
            'id', 'name', 'source_names', 'supplier_names',
            'grade_names', 'batches'
        ]

    def get_source_names(self, obj):
        return [s.name for s in obj.sources.all()]

    def get_supplier_names(self, obj):
        return [s.name for s in obj.suppliers.all()]

    def get_grade_names(self, obj):
        return [g.name for g in obj.grade.all()]

    def get_batches(self, obj):
        batches = ConsumableBatch.objects.filter(consumable=obj)
        return ConsumableBatchSerializer(batches, many=True).data


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drawing
        fields = ['id', 'drawing_title']


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'serial_no', 'last_calibration_date', 'calibration_due_date', 'calibration_certificate']

class EquipmentDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentDocument
        fields = ['id', 'title', 'documentfile', 'release_date', 'approved_by']

class ProcessSerilalizers(serializers.ModelSerializer):
    class Meta:
        model =Process
        fields = '__all__'
class ProductBatchAcceptanceTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatchAcceptanceTest
        fields = [
            'id',
            'product_batch',
            'acceptance_test',
            'result',
            'date_of_test',
            'remarks',
            'report'
        ]

class ProductAcceptanceTestSerializer(serializers.ModelSerializer):
    acceptance_test_name = serializers.CharField(source='acceptance_test.name', read_only=True)
    unit_name = serializers.CharField(source='unit.name', read_only=True)

    class Meta:
        model = ProductAcceptanceTest
        fields = [
            'id',
            'product',                
            'acceptance_test',        
            'acceptance_test_name',   
            'min_value',
            'max_value',
            'unit',                   
            'unit_name',              
            'created_at',
        ]

        
class AcceptanceTestResultSerializer(serializers.ModelSerializer):
    acceptance_test_name = serializers.CharField(source='acceptance_test.test_name')

    class Meta:
        model = AcceptanceTestResult
        fields = ['acceptance_test_name', 'result', 'date_of_test', 'remarks', 'document']


# serializers.py


class AcceptanceTestSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    reevaluation_frequency_days = serializers.SerializerMethodField()

    class Meta:
        model = AcceptanceTest
        fields = [
            'id',
            'name',
            'min_value',
            'max_value',
            'unit',
            'unit_name',
            'reevaluation_frequency_value',
            'reevaluation_frequency_unit',
            'test_type',
            'test_result',
            'specification_result',
            'reevaluation_frequency_days',  # custom timedelta display
        ]

    def get_reevaluation_frequency_days(self, obj):
        return obj.reevaluation_frequency.days if obj.reevaluation_frequency else None


class   RawMaterialAcceptanceTestSerializer(serializers.ModelSerializer):
    raw_material_name = serializers.CharField(source='raw_material.name', read_only=True)
    acceptance_test_name = serializers.CharField(source='acceptance_test.name', read_only=True)
    sources_name = serializers.CharField(source='sources.name', read_only=True)
    suppliers_name = serializers.CharField(source='suppliers.name', read_only=True)
    grade_name = serializers.CharField(source='grade.name', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = RawMaterialAcceptanceTest
        fields = [
            'id',
            'batch_id',
            'raw_material',
            'raw_material_name',
            'acceptance_test',
            'acceptance_test_name',
            'test_value',
            'sources',
            'sources_name',
            'suppliers',
            'suppliers_name',
            'grade',
            'grade_name',
            'min_value',
            'max_value',
            'file',
            'file_url',
            'created_by',
            'status',
            'remark',
        ]

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        elif obj.file:
            return obj.file.url
        return None




class ProductBatchDetailedSerializer(serializers.ModelSerializer):
    process = serializers.ListField(required=False)
    batch_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    # unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), required=False, allow_null=True)
    unit = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    batch_size_value = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    component_batch = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    consumable_batch = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    manufacturings_start_date = serializers.DateField(required=False, allow_null=True)
    manufacturings_end_date = serializers.DateField(required=False, allow_null=True)
    packing_details = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False, allow_null=True)
    raw_material_batch = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = ProductBatchs
        fields = '__all__'






