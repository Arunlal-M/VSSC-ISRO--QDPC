from qdpc.core.modelviewset import BaseModelViewSet
from rest_framework import status
from qdpc.core import constants
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404, render, redirect
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.consumable import Consumable
from qdpc_core_models.models.unit import Unit
from consumable.serializers.consumable_batch_serializer import ConsumableBatchDetailedSerializer, ConsumableBatchSerializer
from consumable.serializers.consumable_acceptance_test_seraizler import ConsumableAcceptanceTestSerializer
from qdpc_core_models.models.acceptance_test import AcceptanceTest
from consumable.services.consumable_service import ConsumableService




class ConsumableBatchFetchView(BaseModelViewSet):
  

    def get(self,request,pk=None):
        if pk:
            data={}
            success = False
            message = constants.USER_FETCH_FAILED
            status_code = status.HTTP_403_FORBIDDEN
            try:
                success, status_code, data, message = ConsumableService.get_consumable_batch_list(pk=None)
                context = {'batches':data}
                return render(request,'consumable_batchlist.html',context)

            except Exception as ex:
                success = False
                message = constants.USER_FETCH_FAILED
                status_code = status.HTTP_400_BAD_REQUEST
                
                return self.render_response(data,success, message, status_code)
        else:
            consumable_batches =self.get_all_obj(model_name=ConsumableBatch)
            serializer = ConsumableBatchSerializer(consumable_batches, many=True)
            context = {'batches': serializer.data}

           
        return render(request,'consumable_batchlist.html',context)
    
   
   

class ConsumableBatchAddView(BaseModelViewSet):

    def get(self,request):
        consumables =self.get_all_obj(model_name=Consumable)
        units = self.get_all_obj(model_name=Unit)
        acceptance_test =self.get_all_obj(model_name=AcceptanceTest)
        consumables_with_expiry = []
        for consumable in consumables:
            consumables_with_expiry.append({
                'id': consumable.id,
                'name': consumable.name,
                'grade': consumable.grade,
                'shelf_life_value': consumable.shelf_life_value,
                'shelf_life_unit': consumable.shelf_life_unit,
            })
        context = {
            'consumables': consumables_with_expiry,
            'units': units,
            'acceptance' : acceptance_test

        }

        return render(request,'consumable_batch.html',context)
    
    def post(self, request):
        success=False
        message=constants.CONSUMABLE_BATCH_FAILD
        status_code=status.HTTP_403_FORBIDDEN
        data=request.data
      
        try:
            if data:
                success, status_code, data, message = ConsumableService.add_consumable_bach_add(data=data)
           
        except Exception as ex:
            success = False
            message = constants.CONSUMABLE_BATCH_FAILD
            status_code = status.HTTP_400_BAD_REQUEST
            
        return self.render_response(data, success, message, status_code)



class ConsumableBatchAcceptenceTest(BaseModelViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        print(request.data, "Received request data")

        consumable_id = request.data.get('consumable')
        batch_id = request.data.get('batch_id')
        sources_id = request.data.get('sources')
        suppliers_id = request.data.get('suppliers')
        grade_id = request.data.get('grade')

        data = []
        index = 0
        while f'acceptance_tests[{index}][id]' in request.data:
            test_data = {
                'batch_id': batch_id,
                'consumable': consumable_id,
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

        serializer = ConsumableAcceptanceTestSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ConsumableBatchDetailView(BaseModelViewSet):
    """
    View to handle detailed list of batchlist.
    """

    def get(self, request, batch_id):
        batch = get_object_or_404(ConsumableBatch, batch_id=batch_id)
        serializer = ConsumableBatchDetailedSerializer(batch)
        return render(request, 'consumable_batch_detail_view.html', {'batch_detail': serializer.data})