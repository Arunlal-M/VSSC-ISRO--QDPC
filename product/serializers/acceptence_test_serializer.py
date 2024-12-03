from rest_framework import serializers
from qdpc_core_models.models.acceptance_test import AcceptanceTest


class AcceptanceTestSerializer(serializers.ModelSerializer):
 
    sampling_plan_url = serializers.SerializerMethodField()
    unit_name = serializers.SerializerMethodField() 

    class Meta:
        model = AcceptanceTest
        fields = [
            'id','name', 
            'min_value', 'max_value', 'unit', 'sampling_plan', 
            'sampling_plan_url', 'unit_name','test_type','test_result',
            'reevaluation_frequency_value', 
            'reevaluation_frequency_unit', 'reevaluation_frequency'
        ]


    def get_sampling_plan_url(self, obj):
        request = self.context.get('request')
        if request is not None and obj.sampling_plan:
            return request.build_absolute_uri(obj.sampling_plan.url)
        elif obj.sampling_plan:
            # Manually construct the URL if request is None
            return f"/product{obj.sampling_plan.url}"
        return None
    

    def get_unit_name(self, obj):
        # Access the unit's name field and return it
        return obj.unit.abbreviation if obj.unit else None
