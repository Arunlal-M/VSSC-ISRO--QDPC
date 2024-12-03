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
    
   
   

class ComponentBatchAddView(BaseModelViewSet):

    def get(self,request):
        components =self.get_all_obj(model_name=Component)
        units = self.get_all_obj(model_name=Unit)
        acceptance_test =self.get_all_obj(model_name=AcceptanceTest)
        components_with_expiry = []
        for component in components:
            components_with_expiry.append({
                'id': component.id,
                'name': component.name,
                'grade': component.grade,
                'shelf_life_value': component.shelf_life_value,
                'shelf_life_unit': component.shelf_life_unit,
            })
        context = {
            'components': components_with_expiry,
            'units': units,
            'acceptance' : acceptance_test

        }

        return render(request,'component_batch.html',context)
    
    def post(self, request):
        success=False
        message=constants.COMPONENT_BATCH_FAILED
        status_code=status.HTTP_403_FORBIDDEN
        data=request.data
      
        try:
            if data:
                success, status_code, data, message = ComponentService.add_component_bach_add(data=data)
           
        except Exception as ex:
            success = False
            message = constants.COMPONENT_BATCH_FAILED
            status_code = status.HTTP_400_BAD_REQUEST
            
        return self.render_response(data, success, message, status_code)



class ComponentBatchAcceptenceTest(BaseModelViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        print(request.data, "Received request data")

        component_id = request.data.get('component')
        batch_id = request.data.get('batch_id')
        sources_id = request.data.get('sources')
        suppliers_id = request.data.get('suppliers')
        grade_id = request.data.get('grade')

        data = []
        index = 0
        while f'acceptance_tests[{index}][id]' in request.data:
            test_data = {
                'batch_id': batch_id,
                'component': component_id,
                'acceptance_test': request.data.get(f'acceptance_tests[{index}][id]'),
                'test_value': request.data.get(f'acceptance_tests[{index}][test_value]'),
                'sources': sources_id,
                'suppliers': suppliers_id,
                'grade': grade_id,
                'min_value': request.data.get(f'acceptance_tests[{index}][min_value]'),
                'max_value': request.data.get(f'acceptance_tests[{index}][max_value]'),
                'file': request.FILES.get(f'acceptance_tests[{index}][file]'),
                'status': request.data.get(f'acceptance_tests[{index}][status]'),
                'remark': request.data.get(f'acceptance_tests[{index}][remark]'),
                'created_by': request.data.get(f'acceptance_tests[{index}][created_by]', 'user')
            }
            data.append(test_data)
            index += 1

        print(data, "Processed test data")

        serializer = ComponentAcceptanceTestSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)