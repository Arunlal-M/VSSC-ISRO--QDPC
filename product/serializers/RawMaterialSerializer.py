from rest_framework import serializers
from qdpc_core_models.models.raw_material import RawMaterial
from product.serializers.source_serializer import SourcesSerializer
from product.serializers.supplier_serializer import SuppliersSerializer
from qdpc_core_models.models.source import Sources
from qdpc_core_models.models.supplier import Suppliers
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.grade import Grade

class RawMaterialSerializer(serializers.ModelSerializer):
    sources = serializers.PrimaryKeyRelatedField(queryset=Sources.objects.all(), many=True)
    suppliers = serializers.PrimaryKeyRelatedField(queryset=Suppliers.objects.all(), many=True)
    acceptance_test = serializers.PrimaryKeyRelatedField(queryset=AcceptanceTest.objects.all(), many=True)
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), many=True)
    calculate_expiry_date = serializers.SerializerMethodField()
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
            'shelf_life_value',
            'acceptance_test',
            'shelf_life_unit',
            'user_defined_date',
            'source_names',
            'supplier_names',
            'grade_names',
            'calculate_expiry_date',
            'acceptance_test_names',
        ]
        
    def validate_shelf_life_value(self, value):
        """Ensure shelf_life_value is numeric (float or integer)."""
        if not isinstance(value, (float, int)):
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

    def create(self, validated_data):
        sources = validated_data.pop('sources', [])
        suppliers = validated_data.pop('suppliers', [])
        grades = validated_data.pop('grade', [])
        acceptance_test = validated_data.pop('acceptance_test', [])

        raw_material = RawMaterial.objects.create(**validated_data)

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