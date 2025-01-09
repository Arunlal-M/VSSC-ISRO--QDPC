from rest_framework import status
from qdpc.core import constants
from component.serializers.component_batch_serializer import ComponentBatchSerializer

from component.serializers.component_serializer import ComponentSerializer
from qdpc_core_models.models.componentbatch import ComponentBatch
from qdpc_core_models.models.component import Component
# from consumable.serializers.consumable_acceptance_test_serializer import ConsumableAcceptanceTestSerializer


class ComponentManager:    

    def component_batch_fetch(cls,pk=None,*args, **kwargs):
        data = {}
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.USER_FETCH_FAILED
      
        try:
            component_batch = ComponentBatch.objects.get(pk=pk)
            serializer = ComponentBatchSerializer(component_batch)
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        except ComponentBatch.DoesNotExist:
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.USER_FETCH_FAILED
      
        return success, status_code,data, message
    
    @classmethod
    def component_batch_add(cls,data,*args, **kwargs):
        print(data,"what data i got")
        serializer = ComponentBatchSerializer(data=data)
        
        if serializer.is_valid():
            print("serilaizer is valid")
            serializer.save()
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        else:
            print("serilaizer nto valid")
            print(serializer.errors)
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.USER_FETCH_FAILED
      
        return success,status_code,data, message
    


    
    
    @classmethod
    def component_add(cls,data,*args, **kwargs):
        print(data,"what data i got")
        serializer = ComponentSerializer(data=data)
      
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
    def component_list_fetch(cls,pk=None,*args, **kwargs):
        data = {}
        print("data found")
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.COMPONENT_FETCH_FAILED
      
        try:
            component_list = Component.objects.get(pk=pk)
            serializer = ComponentSerializer(component_list)
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        except Component.DoesNotExist:
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.COMPONENT_FETCH_FAILED
      
        return success, status_code,data, message





