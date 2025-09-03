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
    def raw_material_batch_add(cls, data, *args, **kwargs):
        try:
            serializer = RawMaterialBatchSerializer(data=data)
            
            if serializer.is_valid():
                batch = serializer.save()
                data = serializer.data
                success = True
                message = "Raw material batch created successfully"
                status_code = status.HTTP_201_CREATED
            else:
                success = False
                status_code = status.HTTP_400_BAD_REQUEST
                message = f"Validation failed: {serializer.errors}"
                data = {}
        except Exception as e:
            success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = f"Error creating batch: {str(e)}"
            data = {}
      
        return success, status_code, data, message
    


    
    
    @classmethod
    def raw_material_add(cls, data, *args, **kwargs):
        try:
            data['is_active'] = True
            serializer = RawMaterialSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                success = True
                message = constants.RETRIVED_USER_SUCCESS
                status_code = status.HTTP_200_OK
            else:
                data = {}
                success = False
                status_code = status.HTTP_400_BAD_REQUEST
                message = f"Validation failed: {serializer.errors}"

            return success, status_code, data, message
            
        except Exception as e:
            data = {}
            success = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = f"Error creating raw material: {str(e)}"
            return success, status_code, data, message
    

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


from product.serializers.product_batch_serializer import ProductBatchDetailedSerializer
from product.serializers.product_serializer import ProductSerializer
from qdpc_core_models.models.product_batchlist import ProductBatch
from qdpc_core_models.models.product import Product


class ProductManager:    

    def product_batch_fetch(cls,pk=None,*args, **kwargs):
        data = {}
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.USER_FETCH_FAILED
      
        try:
            product_batch = ProductBatch.objects.get(pk=pk)
            serializer = ProductBatchDetailedSerializer(product_batch)
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        except ProductBatch.DoesNotExist:
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.USER_FETCH_FAILED
      
        return success, status_code,data, message
    
    @classmethod
    def product_batch_add(cls,data,*args, **kwargs):
        print(data,"what data i got")
        serializer = ProductBatchDetailedSerializer(data=data)
        
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
    def product_add(cls,data,*args, **kwargs):
        print(data,"what data i got")
        serializer = ProductSerializer(data=data)
      
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
    def product_list_fetch(cls,pk=None,*args, **kwargs):
        data = {}
        print("data found")
        success = False
        status_code = status.HTTP_400_BAD_REQUEST
        message = constants.PRODUCT_FETCH_FAILED
      
        try:
            product_list = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product_list)
            data = serializer.data
            success = True
            message = constants.RETRIVED_USER_SUCCESS
            status_code = status.HTTP_200_OK
        except Product.DoesNotExist:
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            message = constants.USER_FETCH_FAILED
      
        return success, status_code,data, message










