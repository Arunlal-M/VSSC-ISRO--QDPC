from rest_framework import status
from qdpc.core import constants
from product.serializers.rawmaterial_batch_serializer import RawMaterialBatchSerializer

from product.serializers.RawMaterialSerializer import RawMaterialSerializer
from qdpc_core_models.models.raw_materialbach import RawMaterialBatch
from qdpc_core_models.models.raw_material import RawMaterial


class RawMatrialManager:    

    def raw_material_batch_fetch(cls,pk=None,*args, **kwargs):
        data = {}
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.USER_FETCH_FAILED
      
        try:
            raw_material_batch = RawMaterialBatch.objects.get(pk=pk)
            serializer = RawMaterialBatchSerializer(raw_material_batch)
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        except RawMaterialBatch.DoesNotExist:
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.USER_FETCH_FAILED
      
        return success, status_code,data, message
    
    @classmethod
    def raw_material_batch_add(cls,data,*args, **kwargs):
        print(data,"what data i got")
        serializer = RawMaterialBatchSerializer(data=data)
        
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
    def raw_material_add(cls,data,*args, **kwargs):
        print(data,"what data i got")
        serializer = RawMaterialSerializer(data=data)
      
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
    def raw_material_list_fetch(cls,pk=None,*args, **kwargs):
        data = {}
        print("data found")
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.RAW_MATERIAL_FETCH_FAILED
      
        try:
            raw_material_list = RawMaterial.objects.get(pk=pk)
            serializer = RawMaterialSerializer(raw_material_list)
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        except RawMaterial.DoesNotExist:
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.USER_FETCH_FAILED
      
        return success, status_code,data, message




