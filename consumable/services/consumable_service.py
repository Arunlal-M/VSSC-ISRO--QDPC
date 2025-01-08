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
        except:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

        return success, status_code, data, message

    @classmethod

    def get_consumable_batch_list(cls,pk=None,*args,**kwargs):
        try:
            consumable_manager = ConsumableManager()
            success, status_code, data, message = consumable_manager.consumable_batch_fetch(pk=None, *args,**kwargs)
        except:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

        return success, status_code, data, message
    


    @classmethod

    def add_consumable_bach_add(cls,data):
        print(data)
        try:
            print(data,"data2")
            consumable_manager = ConsumableManager()
            success, status_code, data, message = consumable_manager.consumable_batch_add(data=data)
        except:
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

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
            message = constants.USER_FETCH_FAILED
            success = False
            status_code = status.HTTP_400_BAD_REQUEST
            data = {"error": "Invalid data"}

        return success, status_code, data, message

