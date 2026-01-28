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
        message = constants.CONSUMABLE_BATCH_FAILD
      
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
            message = constants.CONSUMABLE_BATCH_FAILD
      
        return success, status_code,data, message
    
    @classmethod
    def consumable_batch_add(cls,data,*args, **kwargs):
        try:
            print("Data received in consumable_batch_add:", data)
            
            serializer = ConsumableBatchSerializer(data=data)
            
            if serializer.is_valid():
                print("Serializer is valid")
                batch = serializer.save()
                data = serializer.data
                success = True
                message = "Consumable batch created successfully"
                status_code = status.HTTP_201_CREATED
            else:
                print("Serializer not valid")
                print("Validation errors:", serializer.errors)
                success = False
                status_code = status.HTTP_400_BAD_REQUEST
                message = "Validation failed: " + str(serializer.errors)
                data = {}
        except Exception as e:
            print(f"Error creating consumable batch: {str(e)}")
            import traceback
            traceback.print_exc()
            success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = f"Error creating consumable batch: {str(e)}"
            data = {}
        
        print(f"Final output: success={success}, status_code={status_code}, data={data}, message={message}")
        return success, status_code, data, message
    


    
    
    @classmethod
    def consumable_add(cls,data,*args, **kwargs):
        try:
            print("Data received in consumable_add:", data)
            
            serializer = ConsumableSerializer(data=data)
            
            if serializer.is_valid():
                print("Serializer is valid")
                consumable = serializer.save()
                data = serializer.data
                success = True
                message = "Consumable created successfully"
                status_code = status.HTTP_201_CREATED
            else:
                print("Serializer not valid")
                print("Validation errors:", serializer.errors)
                success = False
                status_code = status.HTTP_400_BAD_REQUEST
                message = "Validation failed: " + str(serializer.errors)
                data = {}
        except Exception as e:
            print(f"Error creating consumable: {str(e)}")
            import traceback
            traceback.print_exc()
            success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = f"Error creating consumable: {str(e)}"
            data = {}
        
        print(f"Final output: success={success}, status_code={status_code}, data={data}, message={message}")
        return success, status_code, data, message
    

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
    





