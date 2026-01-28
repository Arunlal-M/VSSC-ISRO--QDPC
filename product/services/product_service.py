# from qdpc_core_models.models.product_batchlist import ProductBatch
# from product.serializers.product_batch_serializer import ProductBatchDetailedSerializer


# class ProductService:
#     @staticmethod
#     def get_product_batch_detail(pk):
#         # Fetch a specific product batch
#         batch = ProductBatch.objects.select_related(
#             'RawMaterial', 'consumable', 'Component', 'Process', 'batch_size_unit'
#         ).filter(pk=pk).first()
#         if batch:
#             serializer = ProductBatchDetailedSerializer(batch)
#             return True, 200, serializer.data, "Product batch fetched successfully."
#         return False, 404, {}, "Product batch not found."

#     @staticmethod
#     def add_product_batch(data):
#         # Create a new product batch
#         try:
#             batch = ProductBatch.objects.create(**data)
#             return True, 201, {'batch_id': batch.batch_id}, "Product batch created successfully."
#         except Exception as ex:
#             return False, 400, {}, str(ex)
        
        
        
        
from qdpc.core import constants
from django.conf import settings
from rest_framework import status
from qdpc_core_models.models.user import User
from product.core.helpers import ProductManager
import traceback


class ProductService:
    "UserService to make all the user operations"


    @classmethod

    def get_product_list(cls,pk=None,*args,**kwargs):
        try:
            product_manager = ProductManager()
            success, status_code, data, message = product_manager.product_list_fetch(pk=pk, *args,**kwargs)
        except:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

        return success, status_code, data, message

    @classmethod

    def get_product_batch_list(cls,pk=None,*args,**kwargs):
        try:
            product_manager = ProductManager()
            success, status_code, data, message = product_manager.product_batch_fetch(pk=None, *args,**kwargs)
        except:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

        return success, status_code, data, message
    


    @classmethod

    def add_product_batch_add(cls,data):
        print(data)
        try:
            print(data,"data2")
            product_manager = ProductManager()
            success, status_code, data, message = product_manager.product_batch_add(data=data)
        except:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

        return success, status_code, data, message
    
    @classmethod
    def add_product_add(cls, data):
        print(data, "Servicesss")
        try:
            product_manager = ProductManager()
            success, status_code, data, message = product_manager.product_add(data=data)
            print(success, status_code, data, message, "What I obtained after service")
        except Exception as e:
            print("Entered except here")
            print(f"Exception: {e}")
            traceback.print_exc()  # This will print the full traceback
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

        return success, status_code, data, message



