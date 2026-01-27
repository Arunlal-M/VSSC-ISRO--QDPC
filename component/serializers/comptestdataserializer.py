
from rest_framework import serializers
from qdpc_core_models.models.componentGradeAcceptance import ComponentGradeAcceptanceTest

# serializers.py
from rest_framework import serializers
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.grade import Grade

class CompTestDataSerializer(serializers.ModelSerializer):
    component_id = serializers.PrimaryKeyRelatedField(
        queryset=Component.objects.all(), source='component'
    )
    acceptance_test_id = serializers.PrimaryKeyRelatedField(
        queryset=AcceptanceTest.objects.all(), source='acceptance_test'
    )
    grade_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all(), source='grade'
    )

    class Meta:
        model = ComponentGradeAcceptanceTest
        fields = [
            'component_id',
            'acceptance_test_id',
            'grade_id',
            'min_value',
            'max_value',
            'unit_name',
            'reevaluation_frequency',
        ]

    def validate(self, data):
        if data['min_value'] > data['max_value']:
            raise serializers.ValidationError("min_value cannot be greater than max_value.")
        return data
