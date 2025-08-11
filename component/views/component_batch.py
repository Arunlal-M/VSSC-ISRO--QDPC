from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework import status
from qdpc.core import constants
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render, redirect
from qdpc_core_models.models.componentbatch import ComponentBatch
from qdpc_core_models.models.component import Component
from qdpc_core_models.models.unit import Unit
from component.serializers.component_batch_serializer import ComponentBatchSerializer
from component.serializers.component_acceptance_test_serializer import ComponentAcceptanceTestSerializer
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from component.services.component_service import ComponentService
from datetime import datetime, timedelta
from urllib.parse import unquote
from collections import defaultdict
import re
from qdpc_core_models.models.componentGradeAcceptance import ComponentGradeAcceptanceTest


class ComponentBatchFetchView(BaseModelViewSet):
  

    def get(self,request,pk=None):
        if pk:
            data={}
            success = False
            message = constants.USER_FETCH_FAILED
            status_code = status.HTTP_403_FORBIDDEN
            try:
                success, status_code, data, message = ComponentService.get_component_batch_list(pk=None)
                context = {'batches':data}
                return render(request,'component_batchlist.html',context)

            except Exception as ex:
                success = False
                message = constants.USER_FETCH_FAILED
                status_code = status.HTTP_400_BAD_REQUEST
                
                return self.render_response(data,success, message, status_code)
        else:
            component_batches =self.get_all_obj(model_name=ComponentBatch)
            serializer = ComponentBatchSerializer(component_batches, many=True)
            context = {'batches': serializer.data}

           
        return render(request,'component_batchlist.html',context)
    
   
    
   
   
class ComponentBatchEditView(BaseModelViewSet):

    def get(self, request, batch_id):
        try:
            # Fetch the ComponentBatch batch by ID
            component_batch = ComponentBatch.objects.get(batch_id=batch_id)
            serializer = ComponentBatchSerializer(component_batch)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        except ComponentBatch.DoesNotExist:
            return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, batch_id):
        try:
            decoded_batch_id = unquote(batch_id)  # Decode URL-encoded string
            component_batches = ComponentBatch.objects.filter(batch_id=decoded_batch_id)

            if not component_batches.exists():
                return Response({'isSuccess': False, 'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

            print("////////////////////////////////////Received data:", request.data)  # Debugging

            # Expecting a list of units in the request data
            units = request.data.get('units', [])
            if not units:
                return Response({'isSuccess': False, 'detail': 'No units provided'}, status=status.HTTP_400_BAD_REQUEST)

            updated_units = []
            for unit_data in units:
                # Fetch or create a ComponentBatch for each unit
                unit, created = ComponentBatch.objects.update_or_create(
                    batch_id=decoded_batch_id,
                    component_name=unit_data.get('component_name'),
                    defaults={
                        'procurement_date': unit_data.get('procurement_date'),
                        'batch_size_value': unit_data.get('batch_size_value'),
                        'packing_details': unit_data.get('packing_details'),
                        'status': unit_data.get('status'),
                    }
                )
                updated_units.append(unit)

            # Serialize the updated units
            serializer = ComponentBatchSerializer(updated_units, many=True)
            return Response({'isSuccess': True, 'data': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))  # Debugging
            return Response({'isSuccess': False, 'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   

class ComponentBatchAddView(BaseModelViewSet):
    
    def get(self,request):
        grade_name = request.GET.get("grade_name")
        component_name = request.GET.get("component_name")

        # If AJAX request for acceptance tests by grade/raw_material
        if grade_name and component_name:
            print("Grade Name:", grade_name)
            print("component Name:", component_name)
            tests = ComponentGradeAcceptanceTest.objects.filter(
                component__name=component_name,
                grade__name=grade_name
            )
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
        components =self.get_all_obj(model_name=Component)
        units = self.get_all_obj(model_name=Unit)
        acceptance_test =self.get_all_obj(model_name=AcceptanceTest)
        components_with_expiry = []
        for component in components:
            expiry_date = None
            if component.shelf_life_value and component.shelf_life_unit:
                expiry_date = component.calculate_expiry_date  # Ensure the property is used
            components_with_expiry.append({
                'id': component.id,
                'name': component.name,
                'grade': component.grade,
                'shelf_life_value': component.shelf_life_value,
                'shelf_life_unit': component.shelf_life_unit,
                'expiry_date': expiry_date,  # Pass expiry date to template

            })
        context = {
            'components': components_with_expiry,
            'units': units,
            'acceptance' : acceptance_test

        }

        return render(request,'component_batch.html',context)
    
    # def post(self, request):
    #     success=False
    #     message=constants.COMPONENT_BATCH_FAILED
    #     status_code=status.HTTP_403_FORBIDDEN
    #     data=request.data
      
    #     try:
    #         if data:
    #             success, status_code, data, message = ComponentService.add_component_bach_add(data=data)
           
    #     except Exception as ex:
    #         success = False
    #         message = constants.COMPONENT_BATCH_FAILED
    #         status_code = status.HTTP_400_BAD_REQUEST
            
    #     return self.render_response(data, success, message, status_code)

    def post(self, request):
        success=False
        message=constants.COMPONENT_BATCH_FAILED
        status_code=status.HTTP_403_FORBIDDEN
        data=request.data
        
        component_id = data.get("component")
        procurement_date = data.get("procurement_date")

        print("DEBUG - Received Data:", data)  #  Debugging the incoming request
      
        try:
            #  Ensure component_id exists in request
            if not component_id:
                raise ValueError("component ID is missing.")
            
            #  Safely fetch component from DB
            component = Component.objects.filter(id=component_id).first()
            if not component:
                raise ValueError(f"component with ID {component_id} not found.")

            #  Validate procurement date
            if not procurement_date:
                raise ValueError("Procurement date is required to calculate expiry date.")
            
            procurement_date = datetime.strptime(procurement_date, "%Y-%m-%d").date()

            #  Calculate expiry date
            expiry_date = None
            if component.shelf_life_value and component.shelf_life_unit:
                if component.shelf_life_unit == "days":
                    expiry_date = procurement_date + timedelta(days=component.shelf_life_value)
                elif component.shelf_life_unit == "months":
                    expiry_date = procurement_date + timedelta(days=component.shelf_life_value * 30)
                elif component.shelf_life_unit == "years":
                    expiry_date = procurement_date + timedelta(days=component.shelf_life_value * 365)

            #  Ensure expiry date is stored in request data
            data["expiry_date"] = expiry_date

            print("DEBUG - Data Before Service Call:", data)  #  Debugging

            #  Call the service to add the batch
            success, status_code, data, message = ComponentService.add_component_bach_add(data=data)
        except Exception as ex:
            success = False
            message = constants.COMPONENT_BATCH_FAILED
            status_code = status.HTTP_400_BAD_REQUEST
            
        return self.render_response(data, success, message, status_code)


#batch unit this 
class ComponentBatchAcceptenceTest(BaseModelViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        print(request.data, "Received request data")

        component_id = request.data.get('component')
        batch_id = request.data.get('batch_id')

        # Find all unique acceptance_tests keys
        units = defaultdict(list)
        test_indices = set()
        pattern = re.compile(r'acceptance_tests\[(.*?)\]\[id\]')
        for key in request.data.keys():
            match = pattern.match(key)
            if match:
                test_indices.add(match.group(1))

        for idx in test_indices:
            unit_index = request.data.get(f'acceptance_tests[{idx}][unit_index]')
            component_unit = request.data.get(f'acceptance_tests[{idx}][component_unit]')
            sources = request.data.get(f'acceptance_tests[{idx}][source]')
            suppliers = request.data.get(f'acceptance_tests[{idx}][supplier]')
            grade = request.data.get(f'acceptance_tests[{idx}][grade]')

            test_data = {
                'batch_id': batch_id,
                'component': component_id,
                'component_unit': component_unit,
                'sources': sources,
                'suppliers': suppliers,
                'grade': grade,
                'acceptance_test': request.data.get(f'acceptance_tests[{idx}][id]'),
                'test_value': request.data.get(f'acceptance_tests[{idx}][test_value]'),
                'min_value': request.data.get(f'acceptance_tests[{idx}][min_value]'),
                'max_value': request.data.get(f'acceptance_tests[{idx}][max_value]'),
                'file': request.FILES.get(f'acceptance_tests[{idx}][file]'),
                'status': request.data.get(f'acceptance_tests[{idx}][status]'),
                'remark': request.data.get(f'acceptance_tests[{idx}][remark]'),
                'created_by': request.data.get(f'acceptance_tests[{idx}][created_by]', 'user')
            }
            units[unit_index].append(test_data)

        # Now units is a dict: {unit_index: [test1, test2, ...], ...}
        all_tests = []
        for unit_idx, tests in units.items():
            all_tests.extend(tests)

        print(all_tests, "Processed all unit test data")

        serializer = ComponentAcceptanceTestSerializer(data=all_tests, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        
class DeleteComponentBatchView(BaseModelViewSet):
    """
    View to handle the deletion of a source using the POST method.
    """

    def post(self, request, combatchId, format=None):
        try:

            decoded_combatchId = unquote(combatchId)  # Decode URL-encoded string
            componentbatch = ComponentBatch.objects.get(batch_id=decoded_combatchId)
            print(f"Decoded rawbatchId: {decoded_combatchId}")  # Debugging log

            componentbatch.delete()
            return Response({
                'success': True,
                'message': constants.COMPONENT_BATCH_DELETE_SUCCESSFULLY
            }, status=status.HTTP_200_OK)
        except ComponentBatch.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Component Batch not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
        
class ComponentBatchesByMaterial(BaseModelViewSet):
    def get(self, request, material_id):
        batches = ComponentBatch.objects.filter(component_id=material_id)
        serializer = ComponentBatchSerializer(batches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)