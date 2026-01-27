from qdpc.core import constants
from django.conf import settings
from rest_framework import status
# from qdpc_core_models.models.user import User
from consumable.core.helpers import ConsumableManager
import traceback


class ConsumableService:
    "UserService to make all the user operations"


    @classmethod

    def get_consumable_list(cls,pk=None,*args,**kwargs):
        try:
           consumable_manager = ConsumableManager()
           success, status_code, data, message = consumable_manager.consumable_list_fetch(pk=pk, *args,**kwargs)
        except Exception as e:
            print(f"Exception in get_consumable_list: {e}")
            traceback.print_exc()
            message = constants.CONSUMABLE_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Failed to fetch consumable list"}

        return success, status_code, data, message

    @classmethod

    def get_consumable_batch_list(cls,pk=None,*args,**kwargs):
        try:
            consumable_manager = ConsumableManager()
            success, status_code, data, message = consumable_manager.consumable_batch_fetch(pk=None, *args,**kwargs)
        except Exception as e:
            print(f"Exception in get_consumable_batch_list: {e}")
            traceback.print_exc()
            message = constants.CONSUMABLE_BATCH_FAILD
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Failed to fetch consumable batch list"}

        return success, status_code, data, message
    


    @classmethod

    def add_consumable_bach_add(cls,data):
        print(data)
        try:
            print(data,"data2")
            consumable_manager = ConsumableManager()
            success, status_code, data, message = consumable_manager.consumable_batch_add(data=data)
        except Exception as e:
            print(f"Exception in add_consumable_bach_add: {e}")
            traceback.print_exc()
            message = constants.CONSUMABLE_BATCH_FAILD
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Failed to add consumable batch"}

        return success, status_code, data, message
    
    @classmethod
    def add_consumable_add(cls, data):
        print(data, "Servicesss")
        try:
            raw_material_manager = ConsumableManager()
            success, status_code, data, message = raw_material_manager.consumable_add(data=data)
            print(success, status_code, data, message, "What I obtained after service")
        except Exception as e:
            print("Entered except here")
            print(f"Exception: {e}")
            traceback.print_exc()  # This will print the full traceback
            message = constants.CONSUMABLE_BATCH_FAILD
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Failed to add consumable"}

        return success, status_code, data, message

