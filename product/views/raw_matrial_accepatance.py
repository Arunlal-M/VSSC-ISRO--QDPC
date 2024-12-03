from rest_framework import status
from qdpc.core import constants
from rest_framework.response import Response
# from qdpc.services.rawmaterial_service import RawMaterialService
from qdpc.core.modelviewset import BaseModelViewSet
from django.shortcuts import render, redirect
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.unit import Unit
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from product.serializers.acceptence_test_serializer import AcceptanceTestSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Max

class AcceptanceTestAdd(BaseModelViewSet):
    parser_classes = [MultiPartParser, FormParser]

    """ Raw Material List API for qdpc application"""
 
    def get(self, request):
        # raw_material_batch = self.get_all_obj(model_name=RawMaterial)
        units = self.get_all_obj(model_name=Unit)
        context = {
            'units':units
        }
        return render(request, 'acceptance_test.html',context)
    
    def post(self, request):
        # Validate the incoming data using the serializer   
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
            data = {}

        return self.render_response(data, success, message, status_code)


class AcceptanceTestList(BaseModelViewSet):
    """ Raw Material Acceptance Test List API """

    def get(self, request):
        # Get the most recent entry for each AcceptanceTest based on the name
        acceptance_tests = AcceptanceTest.objects.values('name').annotate(latest_id=Max('id'))
        
        # Filter the AcceptanceTest objects to get only the most recent ones
        latest_tests = AcceptanceTest.objects.filter(id__in=[test['latest_id'] for test in acceptance_tests])
        
        # Serialize the filtered results
        test_serializer = AcceptanceTestSerializer(latest_tests, many=True)

        context = {
            'acceptance_tests': test_serializer.data,
        }
        print(context)
        return render(request, 'rmtest-list.html', context)

