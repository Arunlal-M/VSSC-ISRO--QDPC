import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render, redirect
from django.db.models import Max
from datetime import datetime, timedelta


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
from datetime import datetime, timedelta
from urllib.parse import unquote
from qdpc_core_models.models.rawmaterialGradeAcceptance import RawMaterialGradeAcceptanceTest

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
    

    
   
   
class RawMatrialBatchEditView(BaseModelViewSet):

    def get(self, request, batch_id):
        try:
            # Fetch the raw material batch by ID
            raw_material_batch = RawMaterialBatch.objects.get(batch_id=batch_id)
            serializer = RawMaterialBatchSerializer(raw_material_batch)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except RawMaterialBatch.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, batch_id):
        try:
            decoded_batch_id = unquote(batch_id)  # Decode URL-encoded string
            raw_material_batch = RawMaterialBatch.objects.get(batch_id=decoded_batch_id)
        except RawMaterialBatch.DoesNotExist:
            return Response({'isSuccess': False,'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        print("////////////////////////////////////Received data:", request.data)  # Debugging
        
        serializer = RawMaterialBatchSerializer(raw_material_batch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'isSuccess': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'isSuccess': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# class RawMatrialBatchAddView(BaseModelViewSet):

#     def get(self,request):
#         grade_name = request.GET.get("grade_name")
#         raw_material_name = request.GET.get("raw_material_name")
#         if grade_name and raw_material_name:
#             print("Grade Name:", grade_name)
#             print("Raw Material Name:", raw_material_name)
#             tests = RawMaterialGradeAcceptanceTest.objects.filter(
#             raw_material__name=raw_material_name,
#             grade__name=grade_name
#         )

#             result = []
#             for test in tests:
                
#                 result.append({
#                     "id": test.acceptance_test.id,
#                     "name": test.acceptance_test.name,
#                     "min": test.min_value,
#                     "max": test.max_value,
#                     "unit": test.unit_name,
#                 })

#             return Response({"tests": result})
            

#         raw_materials =self.get_all_obj(model_name=RawMaterial)
#         units = self.get_all_obj(model_name=Unit)
#         acceptance_test =self.get_all_obj(model_name=AcceptanceTest)
#         raw_materials_with_expiry = []
#         for raw_material in raw_materials:
#             expiry_date = None
#             if raw_material.shelf_life_value and raw_material.shelf_life_unit:
#                 expiry_date = raw_material.calculate_expiry_date  # Ensure the property is used
#             raw_materials_with_expiry.append({
#                 'id': raw_material.id,
#                 'name': raw_material.name,
#                 'grade': raw_material.grade,
#                 'shelf_life_value': raw_material.shelf_life_value,
#                 'shelf_life_unit': raw_material.shelf_life_unit,
#                 'expiry_date': expiry_date, # Pass expiry date to template

#             })
#         context = {
#             'raw_materials': raw_materials_with_expiry,
#             'units': units,
#             'acceptance' : acceptance_test
#         }

#         return render(request,'batch2.html',context)

class RawMatrialBatchAddView(BaseModelViewSet):

    def get(self, request):
        gradeId = request.GET.get("grade_name")
        raw_materialId = request.GET.get("raw_material_name")
        if gradeId and raw_materialId:            
            tests = RawMaterialGradeAcceptanceTest.objects.filter(
                raw_material=raw_materialId,
                grade=gradeId            )

            result = [
                {
                    "id": test.acceptance_test.id,
                    "name": test.acceptance_test.name,
                    "min": test.min_value,
                    "max": test.max_value,
                    "unit": test.unit_name,
                }
                for test in tests
            ]
            return Response({"tests": result})

        # Main page render
        raw_materials = self.get_all_obj(model_name=RawMaterial)
        units = self.get_all_obj(model_name=Unit)
        acceptance_tests = self.get_all_obj(model_name=AcceptanceTest)       

        raw_materials_with_expiry = [
            {
                'id': rm.id,
                'name': rm.name,
                'grade': rm.grade,
                'shelf_life_value': rm.shelf_life_value,
                'shelf_life_unit': rm.shelf_life_unit,
                'expiry_date': rm.calculate_expiry_date if rm.shelf_life_value and rm.shelf_life_unit else None,
            }
            for rm in raw_materials
        ]

        context = {
            'raw_materials': raw_materials_with_expiry,
            'units': units,
            'acceptance': acceptance_tests
        }
        return render(request, 'batch2.html', context)
    
    

    def post(self, request):
        success = False
        message = "Raw Material Batch Failed"
        status_code = 400
        data = request.data

        raw_material_id = data.get("raw_material")
        procurement_date = data.get("procurement_date")

        if not raw_material_id:
            return self.render_response({}, False, "Raw Material ID is missing.", 400)

        raw_material = RawMaterial.objects.filter(id=raw_material_id).first()
        if not raw_material:
            return self.render_response({}, False, f"Raw Material with ID {raw_material_id} not found.", 400)

        if not procurement_date:
            return self.render_response({}, False, "Procurement date is required.", 400)

        try:
            procurement_date = datetime.strptime(procurement_date, "%Y-%m-%d").date()
        except ValueError:
            return self.render_response({}, False, "Invalid date format. Use YYYY-MM-DD.", 400)

        expiry_date = None
        if raw_material.shelf_life_value and raw_material.shelf_life_unit:
            if raw_material.shelf_life_unit == "days":
                expiry_date = procurement_date + timedelta(days=raw_material.shelf_life_value)
            elif raw_material.shelf_life_unit == "months":
                expiry_date = procurement_date + timedelta(days=raw_material.shelf_life_value * 30)
            elif raw_material.shelf_life_unit == "years":
                expiry_date = procurement_date + timedelta(days=raw_material.shelf_life_value * 365)

        if expiry_date:
            data["expiry_date"] = expiry_date.strftime("%Y-%m-%d")

        try:
            success, status_code, data, message = RawmaterialService.add_rawmaterial_bach_add(data=data)
        except Exception as ex:
            return self.render_response({}, False, f"Unexpected error: {str(ex)}", 500)

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
    
class DeleteRawMatrialBatchView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, rawbatchId, format=None):
        try:
            print(f"RawbatchId received in URL: {rawbatchId}")  # Debugging log

            decoded_rawbatchId = unquote(rawbatchId)  # Decode URL-encoded string
            rawmaterialbatch = RawMaterialBatch.objects.get(batch_id=decoded_rawbatchId)
            print(f"Decoded rawbatchId: {decoded_rawbatchId}")  # Debugging log

            rawmaterialbatch.delete()
            return Response({
                'success': True,
                'message': constants.RAW_MATERIAL_BATCH_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except RawMaterialBatch.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Rawmaterial Batch not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        

class ViewRawMaterialBatchDetailView(BaseModelViewSet):
    """
    View to handle viewing of raw material batch details using POST method.
    """
    def post(self, request, batchId, format=None):
        try:
            batch = RawMaterialBatch.objects.get(batch_id=batchId)
            serializer = RawMaterialBatchSerializer(batch)
            data = serializer.data
            
            return Response({
                'success': True,
                'message': "Raw material batch data fetched successfully.",
                'data': data
            }, status=status.HTTP_200_OK)
        except RawMaterialBatch.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Raw material batch not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RawMaterialBatchesByMaterial(BaseModelViewSet):
    def get(self, request, material_id):
        batches = RawMaterialBatch.objects.filter(raw_material_id=material_id)
        serializer = RawMaterialBatchSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)