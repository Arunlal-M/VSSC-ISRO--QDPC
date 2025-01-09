from rest_framework import status
from qdpc.core import constants
from consumable.serializers.consumable_batch_serializer import ConsumableBatchSerializer

from consumable.serializers.consumable_list_serializer import ConsumableSerializer
from qdpc_core_models.models.consumablebatch import ConsumableBatch
from qdpc_core_models.models.consumable import Consumable
# from consumable.serializers.consumable_acceptance_test_serializer import ConsumableAcceptanceTestSerializer


class ConsumableManager:    

    def consumable_batch_fetch(cls,pk=None,*args, **kwargs):
        data = {}
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.USER_FETCH_FAILED
      
        try:
            consumable_batch = ConsumableBatch.objects.get(pk=pk)
            serializer = ConsumableBatchSerializer(consumable_batch)
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        except ConsumableBatch.DoesNotExist:
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.USER_FETCH_FAILED
      
        return success, status_code,data, message
    
    @classmethod
    def consumable_batch_add(cls,data,*args, **kwargs):
        serializer = ConsumableBatchSerializer(data=data)
        
        if serializer.is_valid():
            print("serilaizer is valid")
            serializer.save()
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        else:
            print("serilaizer not valid")
            print(serializer.errors)
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.USER_FETCH_FAILED
      
        return success,status_code,data, message
    


    
    
    @classmethod
    def consumable_add(cls,data,*args, **kwargs):
        print(data,"what data i got")
        serializer = ConsumableSerializer(data=data)
      
        if serializer.is_valid():
            print("serilaizer is valid")
            serializer.save()
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        else:
            print("Enterd else")
            print(serializer.errors)
            data={}
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.USER_FETCH_FAILED

        
        print (success,status_code,data, message,"Final ouput i got")
        return success,status_code,data, message
    

    @classmethod
    def consumable_list_fetch(cls,pk=None,*args, **kwargs):
        data = {}
        print("data found")
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.CONSUMABLE_FETCH_FAILED
      
        try:
            consumable_list = Consumable.objects.get(pk=pk)
            serializer = ConsumableSerializer(consumable_list)
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        except Consumable.DoesNotExist:
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.CONSUMABLE_FETCH_FAILED
      
        return success, status_code,data, message


# class ConAcceptanceManager:
#     "Used to manage all opeations of the user module"

#     def con_acceptance_fetch(cls, data):
#         serializer =ConsumableAcceptanceTestSerializer(data=data)
#         if serializer.is_valid():
            
#             serializer.save()
#             data = serializer.data
#             success = True
#             message = constants.RETRIVED_USER_SUCCESS
#             status_code = status.HTTP_200_OK
#         else:
#             print("serilaizer nto valid")
#             print(serializer.errors)
#             success = False
#             status_code = status.HTTP_400_BAD_REQUEST
#             message = constants.USER_FETCH_FAILED
      
#         return success,status_code,data, message
    





