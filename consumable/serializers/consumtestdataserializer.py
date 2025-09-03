
from rest_framework import serializers
from qdpc_core_models.models.consumableGradeAcceptance import ConsumableGradeAcceptanceTest

# serializers.py
from rest_framework import serializers
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.grade import Grade

class ConsumTestDataSerializer(serializers.ModelSerializer):
    consumable_id = serializers.PrimaryKeyRelatedField(
        queryset=Consumable.objects.all(), source='consumable'
    )
    acceptance_test_id = serializers.PrimaryKeyRelatedField(
        queryset=AcceptanceTest.objects.all(), source='acceptance_test'
    )
    grade_id = serializers.PrimaryKeyRelatedField(
        queryset=Grade.objects.all(), source='grade'
    )

    class Meta:
        model = ConsumableGradeAcceptanceTest
        fields = [
            'consumable_id',
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
