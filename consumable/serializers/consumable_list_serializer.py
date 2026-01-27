from rest_framework import serializers
from qdpc_core_models.models.consumable import Consumable,PreCertification
from product.serializers.source_serializer import SourcesSerializer
from product.serializers.supplier_serializer import SuppliersSerializer
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.grade import Grade
from django.contrib.contenttypes.models import ContentType


class ConsumableSerializer(serializers.ModelSerializer):
     # Define fields for Many-to-Many relationships
    sources = serializers.PrimaryKeyRelatedField(queryset=Sources.objects.all(), many=True)
    suppliers = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all(), many=True)
    acceptance_test = serializers.PrimaryKeyRelatedField(queryset=AcceptanceTest.objects.all(), many=True)
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), many=True)
    
    # SerializerMethodFields to provide readable names
    calculate_expiry_date = serializers.SerializerMethodField()
    source_names = serializers.SerializerMethodField()
    supplier_names = serializers.SerializerMethodField()
    acceptance_test_names = serializers.SerializerMethodField()
    grade_names = serializers.SerializerMethodField()

    class Meta:
        model = Consumable
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
            'calculate_expiry_date',
            'acceptance_test_names'
        ]

    def validate_shelf_life_value(self, value):
        """Ensure shelf_life_value is numeric (float or integer)."""
        if value is not None and not isinstance(value, (float, int)):
            raise serializers.ValidationError("Shelf life value must be a numeric type.")
        return value
    
    def get_calculate_expiry_date(self, obj):
        return obj.calculate_expiry_date

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

        consumable = Consumable.objects.create(**validated_data)

        # Set many-to-many relationships
        consumable.sources.set(sources)
        consumable.suppliers.set(suppliers)
        consumable.grade.set(grades)
        consumable.acceptance_test.set(acceptance_test)

        return consumable

    def update(self, instance, validated_data):
        sources = validated_data.pop('sources', None)
        suppliers = validated_data.pop('suppliers', None)
        grades = validated_data.pop('grade', None)
        acceptance_test = validated_data.pop('acceptance_test', None)

        instance.name = validated_data.get('name', instance.name)
        instance.shelf_life_value = validated_data.get('shelf_life_value', instance.shelf_life_value)
        instance.shelf_life_unit = validated_data.get('shelf_life_unit', instance.shelf_life_unit)
        # instance.user_defined_date = validated_data.get('user_defined_date', instance.user_defined_date)
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

class PreCertificationSerializer(serializers.ModelSerializer):
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    certificate_file = serializers.FileField(required=True)

    class Meta:
        model = PreCertification
        fields = [
            'id',
            'content_type',
            'object_id',
            'certified_by',
            'certificate_reference_no',
            'certificate_issue_date',
            'certificate_valid_till',
            'certificate_file',
            'certificate_disposition',
        ]