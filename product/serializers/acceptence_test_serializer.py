from rest_framework import serializers
from rest_framework import status
from qdpc_core_models.models.acceptance_test import AcceptanceTest

class AcceptanceTestSerializer(serializers.ModelSerializer):
 
    # sampling_plan_url = serializers.SerializerMethodField()
    unit_name = serializers.SerializerMethodField() 

    class Meta:
        model = AcceptanceTest
        fields = [
            'id','name', 
            'min_value', 'max_value', 'unit', #'sampling_plan',#'sampling_plan_url',
            'unit_name','test_type','test_result',
            'reevaluation_frequency_value', 
            'reevaluation_frequency_unit', 'reevaluation_frequency','specification_result',
        ]

    def validate_name(self, value):
        if AcceptanceTest.objects.filter(name=value).exists():
            raise serializers.ValidationError("An acceptance test with this name already exists.")
        return value

    # def get_sampling_plan_url(self, obj):
    #     request = self.context.get('request')
    #     if request is not None and obj.sampling_plan:
    #         return request.build_absolute_uri(obj.sampling_plan.url)
    #     elif obj.sampling_plan:
    #         return f"/product{obj.sampling_plan.url}"
    #     return None
    
    def get_unit_name(self, obj):
        return obj.unit.abbreviation if obj.unit else None

    def post(self, request):
        serializer = AcceptanceTestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            success = True
            message = 'Acceptance test added successfully!'
            data = serializer.data
            status_code = status.HTTP_201_CREATED
        else:
            success = False
            message = 'Validation failed.'
            status_code = status.HTTP_400_BAD_REQUEST
            data = serializer.errors

        return self.render_response(data, success, message, status_code)
