import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render, redirect
from django.db.models import Max

from qdpc.core.modelviewset import BaseModelViewSet
from qdpc.core import constants

from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.raw_material import RawMaterial
from qdpc_core_models.models.unit import Unit
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from qdpc_core_models.models.raw_material_acceptence_test import RawMaterialAcceptanceTest

from product.serializers.rawmaterial_batch_serializer import RawMaterialBatchDetailedSerializer, RawMaterialBatchSerializer
from product.serializers.raw_material_acceptance_test_seraizler import RawMaterialAcceptanceTestSerializer
from product.serializers.acceptence_test_serializer import AcceptanceTestSerializer

from product.services.raw_material_service import RawmaterialService

from django.shortcuts import get_object_or_404



class RawMatrialBatchFetchView(BaseModelViewSet):
  

    def get(self,request,pk=None):
        if pk:
            data={}
            success = False
            message = constants.USER_FETCH_FAILED
            status_code = status.HTTP_403_FORBIDDEN
            try:
                success, status_code, data, message = RawmaterialService.get_rawmateril_batch_list(pk=None)
                context = {'batches':data}
                return render(request,'batchlist.html',context)

            except Exception as ex:
                success = False
                message = constants.USER_FETCH_FAILED
                status_code = status.HTTP_400_BAD_REQUEST
                
                return self.render_response(data,success, message, status_code)
        else:
            raw_material_batches =self.get_all_obj(model_name=RawMaterialBatch)
            serializer = RawMaterialBatchSerializer(raw_material_batches, many=True)
            context = {'batches': serializer.data}

           
        return render(request,'batchlist.html',context)
    
   
   
class RawMatrialBatchAddView(BaseModelViewSet):

    def get(self,request):
        raw_materials =self.get_all_obj(model_name=RawMaterial)
        units = self.get_all_obj(model_name=Unit)
        acceptance_test =self.get_all_obj(model_name=AcceptanceTest)
        raw_materials_with_expiry = []
        for raw_material in raw_materials:
            raw_materials_with_expiry.append({
                'id': raw_material.id,
                'name': raw_material.name,
                'grade': raw_material.grade,
                'shelf_life_value': raw_material.shelf_life_value,
                'shelf_life_unit': raw_material.shelf_life_unit,
            })
        context = {
            'raw_materials': raw_materials_with_expiry,
            'units': units,
            'acceptance' : acceptance_test
        }

        return render(request,'batch2.html',context)
    
    def post(self, request):
        success=False
        message=constants.RAW_MATERIAL_BATCH_FAILD
        status_code=status.HTTP_403_FORBIDDEN
        data=request.data
      
        try:
            if data:
                success, status_code, data, message = RawmaterialService.add_rawmaterial_bach_add(data=data)
           
        except Exception as ex:
            success = False
            message = constants.RAW_MATERIAL_BATCH_FAILD
            status_code = status.HTTP_400_BAD_REQUEST
            
        return self.render_response(data, success, message, status_code)




# class RawmatrialBatchAcceptenceTest(BaseModelViewSet):

#     parser_classes = (MultiPartParser, FormParser)  # Add parsers to handle file uploads

#     # def post(self, request):
#     #     print(request.data)
#     #     raw_material_id = request.data.get('raw_material')
#     #     acceptance_tests = request.data.getlist('acceptance_tests[]')
#     #     data = []
#     #     for test in acceptance_tests:
#     #         test_data = json.loads(test)
#     #         test_data['raw_material'] = raw_material_id
#     #         data.append(test_data)

#     #     serializer = RawMaterialAcceptanceTestSerializer(data=data, many=True)
#     #     if serializer.is_valid():
#     #         print('IS VALID')
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     else:
#     #         print('NOT VALID')
#     #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def post(self, request):
#         print(request.data)
   
#         # Validate and save the serializer
#         serializer = RawMaterialAcceptanceTestSerializer(data=request.data)
#         if serializer.is_valid():
           
#             serializer.save()  # Calls the custom `create` method in the serializer
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RawmatrialBatchAcceptenceTest(BaseModelViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        print(request.data, "Received request data")

        # Extract common fields from the main request
        raw_material_id = request.data.get('raw_material')
        batch_id = request.data.get('batch_id')
        sources_id = request.data.get('sources')
        suppliers_id = request.data.get('suppliers')
        grade_id = request.data.get('grade')

        # Extract acceptance_tests data as individual entries
        data = []
        index = 0
        while f'acceptance_tests[{index}][id]' in request.data:
            test_data = {
                'batch_id': batch_id,
                'raw_material': raw_material_id,
                'acceptance_test': request.data.get(f'acceptance_tests[{index}][id]'),
                'test_value': request.data.get(f'acceptance_tests[{index}][test_value]'),
                'sources': sources_id,
                'suppliers': suppliers_id,
                'grade': grade_id,
                'min_value': request.data.get(f'acceptance_tests[{index}][min_value]'),  # Corrected bracket
                'max_value': request.data.get(f'acceptance_tests[{index}][max_value]'),  # Corrected bracket
                'file': request.FILES.get(f'acceptance_tests[{index}][file]'),  # Handle file directly
                'status': request.data.get(f'acceptance_tests[{index}][status]'),
                'remark': request.data.get(f'acceptance_tests[{index}][remark]'),
                'created_by': request.data.get(f'acceptance_tests[{index}][created_by]','user')
            }
            data.append(test_data)
            index += 1

        print(data, "Processed test data")

        # Serialize and validate each test data item individually
        serializer = RawMaterialAcceptanceTestSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RawMaterialBatchDetailView(BaseModelViewSet):
    """
    View to handle detailed list of batchlist.
    """

    def get(self, request, batch_id):
        batch = get_object_or_404(RawMaterialBatch, batch_id=batch_id)
        serializer = RawMaterialBatchDetailedSerializer(batch)
        return render(request, 'rawmaterial_batch_detail_view.html', {'batch_detail': serializer.data})